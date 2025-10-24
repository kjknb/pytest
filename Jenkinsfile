pipeline {
    agent any

    environment {
        // ================== 全局环境变量 ==================
        PROJECT_NAME = "pytest_ginchat_api"
        BASE_URL = "http://ginchat-ginchat-app:8080"
        PYTHONPATH = "${WORKSPACE}"
    }

    stages {

        stage('📦 Checkout Code') {
            steps {
                echo "=== 拉取最新代码 ==="
                git branch: 'main',
                    url: 'https://github.com/kjknb/pytest.git',
                    credentialsId: 'github-ssh-key'  // 你在 Jenkins 凭据里配置的 SSH Key ID
            }
        }

        stage('🐍 Install Dependencies') {
            steps {
                echo "=== 安装 Python 依赖环境 ==="
                sh '''
                    set -eux
                    command -v pip3 || apt-get install -y python3-pip
                    pip3 config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
                    pip3 install -r requirements.txt --break-system-packages
                '''
            }
        }

        stage('🧪 Run Tests') {
            steps {
                echo "=== 运行接口自动化测试 ==="
                sh '''
                    export PYTHONPATH=${WORKSPACE}
                    echo "Base URL: ${BASE_URL}"
                    pytest --cache-clear -s -v \
                        --base-url=${BASE_URL} \
                        --alluredir=reports/allure-results
                '''
            }
        }

        stage('📊 Generate Allure Report') {
            steps {
                echo "=== 生成 Allure 报告 ==="
                sh '''
                    allure generate reports/allure-results \
                        -o reports/allure-report --clean
                '''
            }
        }

        stage('📢 Publish Allure Report') {
            steps {
                echo "=== 发布 Allure 报告 ==="
                allure([
                    reportBuildPolicy: 'ALWAYS',
                    results: [[path: 'reports/allure-results']]
                ])
            }
        }
    }

    post {
        always {
            echo "🧹 清理缓存"
            sh 'rm -rf __pycache__ .pytest_cache'
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
