"""
数据库迁移脚本 - Task 2 增强功能
使用 ALTER TABLE 添加新字段（不删除数据）
"""
import sys
from pathlib import Path
import sqlite3

# 添加项目路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def migrate():
    """执行数据库迁移"""
    print("=" * 60)
    print("  Task 2 数据库迁移（保留数据）")
    print("=" * 60)
    
    db_path = project_root / "data" / "app.db"
    
    if not db_path.exists():
        print(f"\n⚠️  数据库不存在，将创建新数据库")
        from backend.app.models import Base
        from backend.app.db import engine
        Base.metadata.create_all(bind=engine)
        print("\n✅ 数据库创建完成！")
        return
    
    print(f"\n📊 连接数据库: {db_path}")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # 检查并添加新字段
        print("\n正在添加新字段...")
        
        new_columns = [
            ("note_id", "INTEGER"),
            ("priority", "VARCHAR(20)"),
            ("category", "VARCHAR(50)"),
            ("assignee", "VARCHAR(100)"),
            ("due_date", "VARCHAR(50)")
        ]
        
        for col_name, col_type in new_columns:
            try:
                cursor.execute(f"ALTER TABLE action_items ADD COLUMN {col_name} {col_type}")
                print(f"  ✅ 添加字段: {col_name}")
            except sqlite3.OperationalError as e:
                if "duplicate column name" in str(e):
                    print(f"  ⏭️  字段已存在: {col_name}")
                else:
                    raise
        
        conn.commit()
        print("\n✅ 迁移完成！\n")
        
        # 显示表结构
        cursor.execute("PRAGMA table_info(action_items)")
        columns = cursor.fetchall()
        
        print("当前 action_items 表结构:")
        for col in columns:
            print(f"  - {col[1]} ({col[2]})")
        
        print("\n新增功能:")
        print("  ✓ ActionItem.note_id (关联到笔记)")
        print("  ✓ ActionItem.priority (优先级: high/medium/low)")
        print("  ✓ ActionItem.category (分类: task/reminder/decision/general)")
        print("  ✓ ActionItem.assignee (负责人)")
        print("  ✓ ActionItem.due_date (截止日期)")
        print("\n  ✓ 创建笔记时自动提取行动项")
        print("  ✓ 行动项包含元数据信息")
        
    except Exception as e:
        print(f"\n❌ 迁移失败: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()
    
    print("\n" + "=" * 60)
    print("\n💡 重启服务器以使用新功能:")
    print("   python start_server_task2_alt.py")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    migrate()
