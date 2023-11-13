# User Information Data Table

> 用户信息数据表

### Front-end：

```cmd
CampusDatabase:
│  
├─admin.html
│
└─tatic
    ├─css
    │      base.css
    │      bootstrap-mini.css
    │      easyui.css
    │      icon.css
    │      ztreestyle.css
    │
    ├─images
    │      accordion_collapse.png
    │      *
    │      *
    │      ztreestandard.gif
    │      ztreestandard.png
    │
    └─js
            easyui-lang-zh_cn.min.js
            *
            *
            jquery-domain.min.js
            ztree-dictionary.js

```

### Back-end：

```cmd
CampusDatabase:
│  
│  Main.py
```

### Data Processing：
```cmd
CampusDatabase:
│  
│  CrawData.py
│  GenDb.py
```
### Json：

```cmd
CampusDatabase:
│  
│  addfrom.json
│  orgTree.json
│  users.json
│  usersType.json
```

### Sqlite3：

```cmd
CampusDatabase:
│  
│  data.db
```

### Usage:

0. Prepare your data file and make sure the token in **Html **and **Main.py** is correctly consistent. （The sample given is a false demonstration data）

1. `pip install -r requirement.txt`
2. `python Main.py`
3. Open the `admin.html` file directly to start using

### Preview

![](.\images\preview.png)
