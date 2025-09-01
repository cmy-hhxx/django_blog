# Django博客系统

基于Django框架构建的现代化博客平台，支持文章发布、用户管理、评论互动等核心功能。

## 核心功能

- **文章管理**：富文本编辑器、标签分类、浏览统计
- **用户系统**：注册登录、个人资料、头像上传
- **评论功能**：树形结构回复、富文本支持
- **后台管理**：Django Admin集成

## 技术栈

- **后端**：Django 4.0 + Python
- **数据库**：SQLite3
- **前端**：Bootstrap + jQuery
- **编辑器**：CKEditor 富文本编辑
- **部署**：uwsgi + nginx

## 项目结构

```
django_blog/
├── articles/          # 文章模块
├── userprofile/       # 用户管理
├── comment/          # 评论系统
├── blog/             # 项目配置
├── templates/        # 模板文件
├── static/          # 静态资源
├── collected_static/ # 生产环境静态文件
└── media/           # 用户上传文件
```

## 主要应用

### Articles（文章模块）
- 文章发布与编辑
- 标签系统（django-taggit）
- 栏目分类管理
- 浏览量统计

### Comment（评论系统）
- 基于MPTT的树形结构
- 多级回复支持
- 富文本评论内容

### UserProfile（用户管理）
- 扩展Django内置用户模型
- 头像上传与个人简介
- 用户资料完善

## 快速启动

1. **环境准备**
   ```bash
   pip install django taggit django-ckeditor django-mptt pillow
   ```

2. **数据库迁移**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **创建超级用户**
   ```bash
   python manage.py createsuperuser
   ```

4. **运行开发服务器**
   ```bash
   python manage.py runserver
   ```

## 配置说明

项目支持邮件通知功能，需在`settings.py`中配置SMTP设置。已集成CKEditor富文本编辑器，支持代码高亮和表情包。

## 部署相关

- 配置文件：`scripts/uwsgi.ini`
- 静态文件收集：`python manage.py collectstatic`
- 已适配nginx反向代理

---

*开发记录详见：[项目开发日志](https://github.com/cmy-hhxx/blog/tree/master/Django)*
