# ============================================
# ✅ 稳定版：清空 docker 中 MySQL 表 user_basic
# ============================================

# 配置信息（请按实际情况修改）
$container = "mysql-docker"   # MySQL 容器名
$user = "root"                # 数据库用户名
$pass = "123456"              # 数据库密码
$db = "ginchat"               # 数据库名
$table = "user_basic"         # 需要清空的表名

Write-Host "🚀 正在清空表: $table ..."

# 检查容器是否运行
$container_status = docker inspect -f '{{.State.Running}}' $container 2>$null
if ($container_status -ne "true") {
    Write-Host "❌ 容器 $container 未运行，请先启动 MySQL 容器"
    exit 1
}

# 等待 MySQL 启动就绪
for ($i = 1; $i -le 10; $i++) {
    $check = docker exec -i $container mysql -u"${user}" -p"${pass}" -e "SELECT 1;" 2>&1
    Write-Host "MySQL检测结果: $check"
    if ($check -match "1") {
        Write-Host "✅ MySQL 已就绪"
        break
    } else {
        Write-Host "⌛ MySQL 未就绪，等待第 $i 次..."
        Start-Sleep -Seconds 3
    }
    if ($i -eq 10) {
        Write-Host "❌ MySQL 启动超时"
        exit 1
    }
}

# 检查数据库是否存在
$db_exists = docker exec -i $container mysql -u"${user}" -p"${pass}" -N -B -e "SHOW DATABASES LIKE '$db';"
Write-Host "数据库检测结果: $db_exists"
if ($db_exists -ne $db) {
    Write-Host "⚠️ 数据库 $db 不存在，跳过清空"
    exit 0
}

# 检查表是否存在
$table_exists = docker exec -i $container mysql -u"${user}" -p"${pass}" -N -B -e "USE $db; SHOW TABLES LIKE '$table';"
Write-Host "数据表检测结果: $table_exists"
if ($table_exists -ne $table) {
    Write-Host "⚠️ 表 $table 不存在，跳过清空"
    exit 0
}

# 执行清空 SQL
$SQL = @"
USE $db;
DELETE FROM $table;
"@

Write-Host "🧹 正在执行删除操作..."
$SQL | docker exec -i $container mysql -u"${user}" -p"${pass}" 2>$null

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ 表 $table 已成功清空！"
} else {
    Write-Host "❌ 清空失败，请检查 MySQL 权限或表名"
}

Write-Host "🎯 操作完成！"
