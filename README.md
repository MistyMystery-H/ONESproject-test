# ONES Project Test

演示并验证三类多对多（many-to-many）关系的示例工程：

| 场景 | 关系 | 说明 |
|------|------|------|
| Identity | Application ↔ IdP | 一个应用可配置多个身份提供商；同一 IdP 可服务多个应用 |
| Database | Microservice ↔ Database | 一个微服务可连接多个数据库；同一数据库可被多个服务查询 |
| Teams | User ↔ Team | 一个用户可加入多个团队；一个团队可包含多个用户 |

## 目录结构

```text
ONESproject-test/
├── README.md
├── requirements.txt
├── pyproject.toml
├── src/
│   └── ones/
│       ├── auth/          # App ↔ IdP
│       ├── database/      # Service ↔ Database
│       └── teams/         # User ↔ Team
└── tests/
    ├── test_idp_app_many_to_many.py
    ├── test_service_db_many_to_many.py
    ├── test_user_team_many_to_many.py
    └── unit/              # 本地可运行的单元测试
```

## 快速开始

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
# source .venv/bin/activate

pip install -r requirements.txt
pip install -e .
```

运行本地单元测试：

```bash
pytest tests/unit -q
```

`tests/` 根目录下的三个用例为原始集成/接口风格测试用例（依赖外部 HTTP 服务或 PostgreSQL），需要按环境配置后再执行。

## 模块说明

- `ones.auth.AuthService`：管理应用与 IdP 的绑定，以及登录与 IdP 不可用时的降级行为
- `ones.database.ServiceDatabaseManager`：管理服务对多库的连接许可与访问记录
- `ones.teams.TeamService`：管理用户与团队的多对多成员关系
