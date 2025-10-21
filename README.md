# pytest_ginchat_api（升级版）

面向 Gin (Go) 项目的企业级接口测试框架：
- 多环境配置（docker/local）
- 自动登录，缓存 token 到 config/token.yaml
- Allure 报告、统一日志
- 从 Swagger 拉取接口元数据（common/swagger_util.py）
- 用户模块：创建、登录、列表、更新、删除

## 安装
pip install -r requirements.txt -i https://pypi.org/simple

## 运行
pytest -s -v --alluredir=reports/allure-results

## 查看 Allure 报告
allure serve reports/allure-results

## 切换环境
修改 config/config.yaml 的 env 值：docker / local
