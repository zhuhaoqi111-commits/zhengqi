#!/usr/bin/env python3
"""
政企智能舆情分析报告生成智能体应用系统
技术栈: Flask + SQLite + layui + 舆情分析
"""

import os
import bcrypt
from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from datetime import datetime
import jieba
import jieba.analyse
import pandas as pd
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import numpy as np

# 创建Flask应用实例
app = Flask(__name__)

# 配置应用
app.config['SECRET_KEY'] = 'zhengqi-secret-key-2024'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///enterprise.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 初始化数据库
db = SQLAlchemy(app)

# 初始化Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = '请先登录'

# 数据模型定义
class User(UserMixin, db.Model):
    """用户模型"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.String(20), default='user')  # user, admin
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    def set_password(self, password):
        """设置密码（加密）"""
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self, password):
        """验证密码"""
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
    
    def is_admin(self):
        """检查是否为管理员"""
        return self.role == 'admin'
    
    def __repr__(self):
        return f'<User {self.username}>'

class Role(db.Model):
    """角色模型"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text)
    permissions = db.Column(db.Text)  # JSON格式存储权限
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class SystemSetting(db.Model):
    """系统设置模型"""
    id = db.Column(db.Integer, primary_key=True)
    app_name = db.Column(db.String(100), default='政企智能舆情分析系统')
    logo_path = db.Column(db.String(200))
    company_name = db.Column(db.String(100))
    contact_info = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class PublicOpinionReport(db.Model):
    """舆情报告模型"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text)
    keywords = db.Column(db.Text)  # 关键词分析结果
    sentiment = db.Column(db.String(20))  # positive, negative, neutral
    source = db.Column(db.String(100))  # 数据来源
    report_date = db.Column(db.Date, nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 关系
    creator = db.relationship('User', backref='reports')

@login_manager.user_loader
def load_user(user_id):
    """加载用户"""
    return User.query.get(int(user_id))

# 舆情分析工具类
class PublicOpinionAnalyzer:
    """舆情分析工具类"""
    
    @staticmethod
    def extract_keywords(text, top_k=10):
        """提取关键词"""
        keywords = jieba.analyse.extract_tags(text, topK=top_k, withWeight=True)
        return keywords
    
    @staticmethod
    def sentiment_analysis(text):
        """简单情感分析"""
        positive_words = ['好', '优秀', '满意', '成功', '进步', '发展', '提升', '改善']
        negative_words = ['差', '问题', '困难', '失败', '下降', '恶化', '投诉', '不满']
        
        positive_count = sum(1 for word in positive_words if word in text)
        negative_count = sum(1 for word in negative_words if word in text)
        
        if positive_count > negative_count:
            return 'positive'
        elif negative_count > positive_count:
            return 'negative'
        else:
            return 'neutral'
    
    @staticmethod
    def generate_report(title, content, source='手动输入'):
        """生成舆情报告"""
        keywords = PublicOpinionAnalyzer.extract_keywords(content)
        sentiment = PublicOpinionAnalyzer.sentiment_analysis(content)
        
        return {
            'title': title,
            'content': content,
            'keywords': keywords,
            'sentiment': sentiment,
            'source': source,
            'report_date': datetime.now().date()
        }

# 路由定义
@app.route('/')
def index():
    """首页"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """登录页面"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            user.last_login = datetime.utcnow()
            db.session.commit()
            
            flash('登录成功！', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard'))
        else:
            flash('用户名或密码错误！', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """用户注册页面"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # 验证表单数据
        if not username or not password or not confirm_password:
            flash('请填写所有必填字段！', 'error')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('两次输入的密码不一致！', 'error')
            return render_template('register.html')
        
        if len(password) < 6:
            flash('密码长度至少6位！', 'error')
            return render_template('register.html')
        
        # 检查用户名是否已存在
        if User.query.filter_by(username=username).first():
            flash('用户名已存在！', 'error')
            return render_template('register.html')
        
        # 创建新用户
        try:
            email = f"{username}@default.com"  # 生成默认邮箱
            user = User(username=username, email=email, role='user')
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            
            flash('注册成功！请登录。', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash('注册失败，请重试！', 'error')
            return render_template('register.html')
    
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    """退出登录"""
    logout_user()
    flash('您已成功退出登录。', 'success')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    """仪表板页面"""
    # 获取统计数据
    user_count = User.query.count()
    report_count = PublicOpinionReport.query.count()
    
    # 获取最近的报告
    recent_reports = PublicOpinionReport.query.order_by(PublicOpinionReport.created_at.desc()).limit(5).all()
    
    return render_template('dashboard.html', 
                         user_count=user_count,
                         report_count=report_count,
                         recent_reports=recent_reports)

@app.route('/admin/users')
@login_required
def admin_users():
    """用户管理页面"""
    if not current_user.is_admin():
        flash('权限不足！', 'error')
        return redirect(url_for('dashboard'))
    
    users = User.query.all()
    return render_template('admin_users.html', users=users)

@app.route('/admin/settings')
@login_required
def admin_settings():
    """系统设置页面"""
    if not current_user.is_admin():
        flash('权限不足！', 'error')
        return redirect(url_for('dashboard'))
    
    settings = SystemSetting.query.first()
    if not settings:
        settings = SystemSetting()
        db.session.add(settings)
        db.session.commit()
    
    return render_template('admin_settings.html', settings=settings)

@app.route('/opinion/reports')
@login_required
def opinion_reports():
    """舆情报告页面"""
    reports = PublicOpinionReport.query.order_by(PublicOpinionReport.created_at.desc()).all()
    return render_template('opinion_reports.html', reports=reports)

@app.route('/opinion/generate', methods=['GET', 'POST'])
@login_required
def generate_opinion_report():
    """生成舆情报告"""
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        source = request.form.get('source', '手动输入')
        
        if title and content:
            # 生成报告
            report_data = PublicOpinionAnalyzer.generate_report(title, content, source)
            
            # 保存到数据库
            report = PublicOpinionReport(
                title=report_data['title'],
                content=report_data['content'],
                keywords=str(report_data['keywords']),
                sentiment=report_data['sentiment'],
                source=report_data['source'],
                report_date=report_data['report_date'],
                created_by=current_user.id
            )
            
            db.session.add(report)
            db.session.commit()
            
            flash('舆情报告生成成功！', 'success')
            return redirect(url_for('opinion_reports'))
        else:
            flash('请填写标题和内容！', 'error')
    
    return render_template('generate_report.html')

@app.route('/api/opinion/analyze', methods=['POST'])
@login_required
def api_analyze_opinion():
    """舆情分析API"""
    data = request.get_json()
    
    if not data or not data.get('content'):
        return jsonify({'error': '内容不能为空'}), 400
    
    content = data['content']
    
    # 关键词提取
    keywords = PublicOpinionAnalyzer.extract_keywords(content)
    
    # 情感分析
    sentiment = PublicOpinionAnalyzer.sentiment_analysis(content)
    
    return jsonify({
        'keywords': keywords,
        'sentiment': sentiment,
        'summary': f'分析完成，共提取{len(keywords)}个关键词，情感倾向为{"积极" if sentiment == "positive" else "消极" if sentiment == "negative" else "中性"}。'
    }), 200

@app.route('/api/opinion/report/<int:report_id>')
@login_required
def api_get_report_detail(report_id):
    """获取报告详情API"""
    report = PublicOpinionReport.query.get_or_404(report_id)
    
    # 检查权限（只能查看自己创建的报告或管理员可以查看所有报告）
    if report.created_by != current_user.id and not current_user.is_admin():
        return jsonify({'error': '权限不足'}), 403
    
    return jsonify({
        'id': report.id,
        'title': report.title,
        'content': report.content,
        'keywords': report.keywords if report.keywords else "[]",
        'sentiment': report.sentiment,
        'source': report.source,
        'created_at': report.created_at.strftime('%Y-%m-%d %H:%M'),
        'created_by': report.creator.username
    }), 200

# API 路由
@app.route('/api/user/add', methods=['POST'])
@login_required
def api_add_user():
    """添加用户API"""
    if not current_user.is_admin():
        return jsonify({'error': '权限不足'}), 403
    
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': '用户名和密码是必填项'}), 400
    
    # 检查用户名是否已存在
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': '用户名已存在'}), 400
    
    # 生成默认邮箱
    email = data.get('email', f"{data['username']}@default.com")
    user = User(username=data['username'], email=email, role=data.get('role', 'user'))
    user.set_password(data['password'])
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'message': '用户添加成功', 'user_id': user.id}), 201

@app.route('/api/settings/update', methods=['POST'])
@login_required
def api_update_settings():
    """更新系统设置API"""
    if not current_user.is_admin():
        return jsonify({'error': '权限不足'}), 403
    
    data = request.get_json()
    settings = SystemSetting.query.first()
    
    if not settings:
        settings = SystemSetting()
        db.session.add(settings)
    
    if 'app_name' in data:
        settings.app_name = data['app_name']
    if 'logo_path' in data:
        settings.logo_path = data['logo_path']
    if 'company_name' in data:
        settings.company_name = data['company_name']
    if 'contact_info' in data:
        settings.contact_info = data['contact_info']
    
    db.session.commit()
    
    return jsonify({'message': '系统设置更新成功'}), 200

# 初始化数据库
def create_tables():
    """创建数据库表"""
    with app.app_context():
        db.create_all()
        
        # 添加默认管理员用户
        if User.query.count() == 0:
            admin_user = User(username='admin', email='admin@zhengqi.com', role='admin')
            admin_user.set_password('admin123')
            db.session.add(admin_user)
            
            # 添加普通用户
            user1 = User(username='user1', email='user1@zhengqi.com', role='user')
            user1.set_password('user123')
            db.session.add(user1)
            
            # 添加默认系统设置
            settings = SystemSetting(app_name='政企智能舆情分析报告生成智能体应用系统')
            db.session.add(settings)
            
            db.session.commit()
            print("数据库初始化完成，默认用户和设置已添加")

# 数据抓取模块路由
@app.route('/crawler')
@login_required
def crawler_page():
    """数据抓取页面"""
    return render_template('crawler.html')

@app.route('/api/crawler/search', methods=['POST'])
@login_required
def api_crawler_search():
    """数据抓取搜索API"""
    try:
        data = request.get_json()
        
        if not data or not data.get('keyword'):
            return jsonify({
                'success': False,
                'message': '关键词不能为空'
            }), 400
        
        keyword = data['keyword']
        max_results = data.get('max_results', 10)
        
        # 导入数据抓取模块
        from data_crawler import NewsCrawler
        
        # 创建抓取器实例
        crawler = NewsCrawler()
        
        # 搜索新闻
        results = crawler.search_news(keyword, max_results)
        
        # 如果基本搜索没有结果，尝试高级搜索
        if not results:
            results = crawler.advanced_search(keyword, max_results)
        
        return jsonify({
            'success': True,
            'data': results,
            'message': f'成功获取 {len(results)} 条新闻数据'
        }), 200
        
    except Exception as e:
        import traceback
        print(f"数据抓取错误: {str(e)}")
        print(traceback.format_exc())
        
        return jsonify({
            'success': False,
            'message': f'数据抓取失败: {str(e)}',
            'data': []
        }), 500

@app.route('/api/crawler/test')
@login_required
def api_crawler_test():
    """数据抓取测试API"""
    try:
        # 导入数据抓取模块
        from data_crawler import NewsCrawler
        
        # 创建抓取器实例
        crawler = NewsCrawler()
        
        # 测试搜索
        results = crawler.search_news('测试', 3)
        
        return jsonify({
            'success': True,
            'data': results,
            'message': f'测试成功，获取到 {len(results)} 条测试数据'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'测试失败: {str(e)}'
        }), 500

# 在应用启动时初始化数据库
create_tables()

if __name__ == '__main__':
    # 创建数据库目录
    os.makedirs('data', exist_ok=True)
    
    # 运行应用
    app.run(debug=True, host='0.0.0.0', port=5000)