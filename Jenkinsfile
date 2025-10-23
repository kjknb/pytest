pipeline {
    agent any

    environment {
        // 飞书机器人 webhook 地址（替换为你的）
        FEISHU_WEBHOOK = "https://open.feishu.cn/open-apis/bot/v2/hook/47e139e1-1a4f-49f1-b8f1-20e7f85af93d"

        // 项目名称（可在通知中使用）
        PROJECT_NAME = "pytest_ginchat_api"
    }

    stages {

        stage('📦 Checkout Code') {
            steps {
                echo "=== 拉取最新代码 ==="
                git branch: 'main', url: 'https://github.com/your-org/pytest_ginchat_api.git'
            }
        }

        stage('🐍 Setup Python Environment') {
            steps {
                echo "=== 创建虚拟环境并安装依赖 ==="
                sh '''
                python -m venv venv
                source venv/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        stage('🧪 Run API Tests') {
            steps {
                echo "=== 执行接口自动化测试 ==="
                sh '''
                source venv/bin/activate
                pytest --cache-clear -s -v --alluredir=reports/allure-results
                '''
            }
        }

        stage('📊 Generate Allure Report') {
            steps {
                echo "=== 生成 Allure 报告 ==="
                sh '''
                allure generate reports/allure-results -o reports/allure-report --clean
                '''
            }
        }

        stage('📢 Publish Report') {
            steps {
                echo "=== 发布 Allure 报告 ==="
                allure includeProperties: false, jdk: '', results: [[path: 'reports/allure-results']]
            }
        }
    }

    post {
        success {
            echo "✅ 测试全部通过，发送飞书通知"
            sh '''
            python common/notify_feishu.py "✅ 项目: ${PROJECT_NAME}\\n构建号: ${BUILD_NUMBER}\\n状态: 成功 🎉\\n报告地址: ${BUILD_URL}"
            '''
        }
        failure {
            echo "❌ 测试失败，发送飞书警报"
            sh '''
            python common/notify_feishu.py "❌ 项目: ${PROJECT_NAME}\\n构建号: ${BUILD_NUMBER}\\n状态: 失败 🚨\\n报告地址: ${BUILD_URL}"
            '''
        }
        always {
            echo "🧹 清理环境并存档测试报告"
            archiveArtifacts artifacts: 'reports/**, logs/**', fingerprint: true
        }
    }
}
