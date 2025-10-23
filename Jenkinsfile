pipeline {
    agent any

    environment {
        BASE_URL = "http://ginchat-ginchat-app:8080"
        REPORT_DIR = "reports/allure-results"
    }

    stages {
        stage('📦 Checkout Code') {
            steps {
                echo "=== 拉取最新代码 ==="
                git branch: 'main', url: 'https://github.com/kjknb/pytest.git'
            }
        }

        stage('🐍 Install Dependencies') {
            steps {
                echo "=== 安装 Python 依赖环境 ==="
                sh '''
                if ! command -v pip3 >/dev/null 2>&1; then
                    apt-get update && apt-get install -y python3 python3-pip
                fi
                pip3 install -r requirements.txt --break-system-packages || true
                pip3 install pytest requests allure-pytest pyyaml pytest-dependency pytest-base-url pytest-html pytest-metadata --break-system-packages
                '''
            }
        }

        stage('🧪 Run Tests') {
            steps {
                echo "=== 运行接口自动化测试 ==="
                sh '''
                export PYTHONPATH=$WORKSPACE
                echo "Base URL: $BASE_URL"
                pytest --cache-clear -s -v --alluredir=$REPORT_DIR --base-url=$BASE_URL
                '''
            }
        }

        stage('📊 Generate Allure Report') {
            when {
                expression { fileExists('reports/allure-results') }
            }
            steps {
                echo "=== 生成 Allure 报告 ==="
                sh 'allure generate reports/allure-results -o reports/allure-report --clean'
            }
        }

        stage('📢 Publish Allure Report') {
            steps {
                allure([
                    includeProperties: false,
                    results: [[path: 'reports/allure-results']]
                ])
            }
        }
    }

    post {
        always {
            echo "🧹 清理缓存"
            sh 'rm -rf __pycache__ .pytest_cache || true'
        }
        success {
            echo "✅ 测试成功"
            sh 'python3 common/notify_feishu.py ✅ pytest_ginchat_api 测试通过 🎉'
        }
        failure {
            echo "❌ 测试失败"
            sh 'python3 common/notify_feishu.py ❌ pytest_ginchat_api 测试失败，请查看 Jenkins 报告！'
        }
    }
}
