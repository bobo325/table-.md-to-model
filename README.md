# 作用
数据库设计表转化为 model

# 用法
快捷键:
```
ctr + shift + alt + k
```

# 转换文本格式
```markdown
## 会员信息表 (member)

| 参数列         | 参数类型      | 描述         |
| -------------- | ------------ | ------------ |
| id             | bigint       | 主键ID       |
| name           | varchar(255) | 名称         |
| longitude      | float        | 经度         |
| description    | text         | 描述         |
| create_time    | datetime     | 创建时间      |
| status         | int          | 状态          |
| is_delete      | bool         | 是否删除      |
| supply_date    | date         | 上市时间      |
```

# 转换之后的文本格式
```python
class Member(db.Model):
    """会员信息表."""
    __tablename__ = 'member'
    # 主键ID
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    # 名称
    name = db.Column(db.String(255))
    # 经度
    longitude = db.Column(db.Float)
    # 描述
    description = db.Column(db.Text)
    # 创建时间
    create_time = db.Column(db.DateTime)
    # 1-已提交 2-通过 3-未通过
    status = db.Column(db.Integer)
    # 是否删除
    is_delete = db.Column(db.Boolean)
    # 上市时间（2018-07-10）
    supply_date = db.Column(db.Date)

```
