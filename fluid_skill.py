import sys
import os
import time
import math
import json
import argparse

# 尝试导入 Chroma (如果环境支持)
try:
    import chromadb
    from chromadb.config import Settings
    HAS_CHROMA = True
except ImportError:
    HAS_CHROMA = False

# 配置路径
WORKSPACE_ROOT = os.path.expanduser(r"~/.openclaw/workspace")
CHROMA_PATH = os.path.join(WORKSPACE_ROOT, r"database\chroma_store")

class FluidMemorySkill:
    def __init__(self):
        self.use_vector = HAS_CHROMA
        
        if self.use_vector:
            # 初始化 Chroma (持久化模式)
            try:
                # 适配 Chroma 0.4+ / 0.5+ API
                if hasattr(chromadb, 'PersistentClient'):
                    self.client = chromadb.PersistentClient(path=CHROMA_PATH)
                else:
                    self.client = chromadb.Client(Settings(
                        persist_directory=CHROMA_PATH,
                        anonymized_telemetry=False
                    ))
                
                self.collection = self.client.get_or_create_collection(name="fluid_memory")
            except Exception as e:
                print(f"[WARN] Chroma 初始化失败: {e}，降级为模拟模式。")
                self.use_vector = False
        
        # 如果没有向量库，回退到 SQLite (这里为了简化，如果降级直接报错提示用户)
        if not self.use_vector:
            print("[INFO] 正在运行在无向量模式 (关键词匹配)")

    def _calculate_score(self, similarity, created_at, access_count):
        """核心流体公式"""
        LAMBDA_DECAY = 0.05  # 遗忘速度
        ALPHA_BOOST = 0.2    # 强化力度
        
        days_passed = (time.time() - created_at) / 86400
        decay = math.exp(-LAMBDA_DECAY * days_passed)
        boost = ALPHA_BOOST * math.log(1 + access_count)
        
        # 相似度在 Chroma 里是距离 (0~2)，需要转换。
        # 假设用的是 cosine distance: score = 1 - distance
        # 这里 similarity 传入时已经是归一化的分数了
        return (similarity * decay) + boost

    def remember(self, content):
        """植入记忆"""
        mem_id = f"mem_{int(time.time()*1000)}"
        now = time.time()
        
        if self.use_vector:
            try:
                self.collection.add(
                    documents=[content],
                    metadatas=[{
                        "created_at": now,
                        "last_accessed": now,
                        "access_count": 0,
                        "status": "active"
                    }],
                    ids=[mem_id]
                )
                return f"[OK] 已植入向量大脑: [{content}]"
            except Exception as e:
                return f"[ERROR] 向量植入失败: {e}"
        else:
            return "[ERROR] 缺少 Chroma 支持，无法植入向量记忆。"

    def recall(self, query):
        """唤起记忆 (Vector + Fluid Logic)"""
        if not self.use_vector:
            return "[ERROR] 缺少 Chroma 支持，无法进行语义检索。"

        try:
            # 1. 粗召回：让 Chroma 找最像的 Top 10 (活跃记忆)
            results = self.collection.query(
                query_texts=[query],
                n_results=10,
                where={"status": "active"} # 只找活跃的
            )
        except Exception as e:
            return f"[ERROR] 检索失败: {e}"

        if not results['ids'][0]:
            return "[EMPTY] 没有找到相关记忆。"

        scored_memories = []
        ids = results['ids'][0]
        docs = results['documents'][0]
        metas = results['metadatas'][0]
        distances = results['distances'][0]

        for i in range(len(ids)):
            # 转换距离为相似度 (通用公式)
            dist = distances[i]
            sim = 1.0 / (1.0 + dist)
            
            meta = metas[i]
            created_at = meta.get('created_at', time.time())
            access_count = meta.get('access_count', 0)
            
            # 计算最终得分
            final_score = self._calculate_score(sim, created_at, access_count)
            
            # Debug info
            print(f"[DEBUG] Doc: {docs[i][:15]}... | Dist: {dist:.3f} -> Sim: {sim:.3f} | Score: {final_score:.3f}")

            if final_score > 0.05: # 降低阈值
                scored_memories.append({
                    "content": docs[i],
                    "score": round(final_score, 3),
                    "id": ids[i],
                    "meta": meta
                })

        # 3. 排序取 Top 3
        scored_memories.sort(key=lambda x: x['score'], reverse=True)
        top_memories = scored_memories[:3]

        # 4. 强化机制 (Boost): 更新 Metadata
        if top_memories:
            for mem in top_memories:
                new_count = mem['meta']['access_count'] + 1
                self.collection.update(
                    ids=[mem['id']],
                    metadatas=[{
                        "created_at": mem['meta']['created_at'],
                        "last_accessed": time.time(),
                        "access_count": new_count,
                        "status": "active"
                    }]
                )
            
            # 格式化输出供 OpenClaw 读取
            return json.dumps([{
                "text": m["content"], 
                "score": m["score"]
            } for m in top_memories], ensure_ascii=False)
        else:
            return "[EMPTY] 记忆存在但权重过低，已被大脑过滤。"

    def forget(self, keyword):
        """主动遗忘 (软删除/归档)"""
        # 这里的实现比较 trick，因为 Chroma 的 update 需要 id
        # 我们先 query 找到它，再 update metadata
        if not self.use_vector: return "[ERROR] No Vector DB"
        
        results = self.collection.query(
            query_texts=[keyword],
            n_results=1, # 假设用户只想删最匹配的那条
            where={"status": "active"}
        )
        
        if results['ids'][0]:
            target_id = results['ids'][0][0]
            target_text = results['documents'][0][0]
            current_meta = results['metadatas'][0][0]
            
            # 更新状态为 archive
            current_meta['status'] = 'archive'
            self.collection.update(
                ids=[target_id],
                metadatas=[current_meta]
            )
            return f"[ARCHIVED] 已归档记忆: '{target_text}'"
        else:
            return "[404] 未找到相关活跃记忆。"

    def status(self):
        if not self.use_vector: return "Mode: Keyword (No Chroma)"
        count = self.collection.count()
        return json.dumps({"total_vectors": count, "backend": "ChromaDB"})

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["remember", "recall", "forget", "status"])
    parser.add_argument("--content", help="Content")
    parser.add_argument("--query", help="Query")
    
    args = parser.parse_args()
    skill = FluidMemorySkill()
    
    if args.action == "remember" and args.content:
        print(skill.remember(args.content))
    elif args.action == "recall" and args.query:
        print(skill.recall(args.query))
    elif args.action == "forget" and args.content:
        print(skill.forget(args.content))
    elif args.action == "status":
        print(skill.status())
