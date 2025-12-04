// 政企管理系统 - 主JavaScript文件

// 页面加载完成后执行
document.addEventListener('DOMContentLoaded', function() {
    console.log('政企管理系统已加载');
    
    // 添加页面加载动画
    const mainContent = document.querySelector('.main-content');
    if (mainContent) {
        mainContent.style.opacity = '0';
        mainContent.style.transition = 'opacity 0.5s ease-in';
        
        setTimeout(() => {
            mainContent.style.opacity = '1';
        }, 100);
    }
    
    // 卡片悬停效果增强
    const featureCards = document.querySelectorAll('.feature-card');
    const statCards = document.querySelectorAll('.stat-card');
    
    featureCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.cursor = 'pointer';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.cursor = 'default';
        });
    });
    
    statCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.cursor = 'pointer';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.cursor = 'default';
        });
    });
    
    // 导航栏激活状态
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (href === currentPath || (href !== '/' && currentPath.startsWith(href))) {
            link.style.color = 'var(--primary-color)';
            link.style.fontWeight = '600';
        }
    });
    
    // 初始化API调用
    initializeDashboard();
});

// 仪表板初始化
function initializeDashboard() {
    if (window.location.pathname === '/dashboard') {
        // 获取用户数据
        fetch('/api/users')
            .then(response => response.json())
            .then(users => {
                console.log('用户数据:', users);
            })
            .catch(error => {
                console.error('获取用户数据失败:', error);
            });
        
        // 获取部门数据
        fetch('/api/departments')
            .then(response => response.json())
            .then(departments => {
                console.log('部门数据:', departments);
            })
            .catch(error => {
                console.error('获取部门数据失败:', error);
            });
        
        // 获取项目数据
        fetch('/api/projects')
            .then(response => response.json())
            .then(projects => {
                console.log('项目数据:', projects);
            })
            .catch(error => {
                console.error('获取项目数据失败:', error);
            });
    }
}

// 工具函数
const Utils = {
    // 显示消息提示
    showMessage: function(message, type = 'info') {
        const messageTypes = {
            'info': { bgColor: '#1890ff', icon: 'ℹ️' },
            'success': { bgColor: '#52c41a', icon: '✅' },
            'warning': { bgColor: '#faad14', icon: '⚠️' },
            'error': { bgColor: '#ff4d4f', icon: '❌' }
        };
        
        const config = messageTypes[type] || messageTypes.info;
        
        const messageHtml = `
            <div class="message-toast" style="
                position: fixed;
                top: 20px;
                right: 20px;
                background: ${config.bgColor};
                color: white;
                padding: 1rem 1.5rem;
                border-radius: 6px;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
                z-index: 9999;
                display: flex;
                align-items: center;
                gap: 0.5rem;
                max-width: 300px;
                animation: slideIn 0.3s ease;
            ">
                <span style="font-size: 1.2rem;">${config.icon}</span>
                <span>${message}</span>
            </div>
        `;
        
        // 添加CSS动画
        if (!document.querySelector('#message-styles')) {
            const style = document.createElement('style');
            style.id = 'message-styles';
            style.textContent = `
                @keyframes slideIn {
                    from { transform: translateX(100%); opacity: 0; }
                    to { transform: translateX(0); opacity: 1; }
                }
                @keyframes slideOut {
                    from { transform: translateX(0); opacity: 1; }
                    to { transform: translateX(100%); opacity: 0; }
                }
            `;
            document.head.appendChild(style);
        }
        
        // 在页面右上角显示消息
        document.body.insertAdjacentHTML('beforeend', messageHtml);
        
        // 3秒后自动移除
        setTimeout(() => {
            const toast = document.querySelector('.message-toast');
            if (toast) {
                toast.style.animation = 'slideOut 0.3s ease';
                setTimeout(() => toast.remove(), 300);
            }
        }, 3000);
    },
    
    // 格式化日期
    formatDate: function(date) {
        return new Date(date).toLocaleDateString('zh-CN', {
            year: 'numeric',
            month: '2-digit',
            day: '2-digit',
            hour: '2-digit',
            minute: '2-digit'
        });
    },
    
    // 防抖函数
    debounce: function(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },
    
    // 添加用户
    addUser: function(userData) {
        return fetch('/api/user/add', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(userData)
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                throw new Error(data.error);
            }
            return data;
        });
    }
};

// 全局错误处理
window.addEventListener('error', function(e) {
    console.error('全局错误:', e.error);
    Utils.showMessage('发生了一个错误，请检查控制台', 'error');
});

// 未捕获的Promise错误处理
window.addEventListener('unhandledrejection', function(e) {
    console.error('未处理的Promise错误:', e.reason);
    Utils.showMessage('发生了一个异步错误，请检查控制台', 'error');
    e.preventDefault();
});