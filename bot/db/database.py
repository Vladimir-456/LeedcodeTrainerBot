import asyncpg
import os
from typing import Optional


class Database:
    def __init__(self):
        self._pool: Optional[asyncpg.pool.Pool] = None

    async def connect(self):
        self._pool = await asyncpg.create_pool(os.getenv("DATABASE_URL"))

    async def close(self):
        if self._pool is not None:
            await self._pool.close()

    async def create_table(self):
        assert self._pool is not None
        async with self._pool.acquire() as conn:
            await conn.execute(
                """
                CREATE TABLE IF NOT EXISTS users(
                    id SERIAL PRIMARY KEY,
                    tg_id BIGINT NOT NULL UNIQUE,
                    username TEXT,
                    created_at TIMESTAMPTZ DEFAULT now()
                )
                """
            )

    async def add_user(self, tg_id: int, username: str | None):
        assert self._pool is not None
        async with self._pool.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO users(tg_id, username)
                VALUES ($1, $2)
                ON CONFLICT (tg_id) DO NOTHING
                """,
                tg_id,
                username,
            )
    async def add_leetcode_username(self, tg_id: int, username: str):
        assert self._pool is not None
        async with self._pool.acquire() as conn:
            await conn.execute(
            """
            UPDATE users
            SET leetcode_username = $2
            WHERE tg_id = $1
            """,
            tg_id,
            username,
        )

    async def get_random_problem_by_difficulty(self, difficulty: str, user_id: int):
        assert self._pool is not None
        async with self._pool.acquire() as conn:
           row = await conn.fetchrow(
               """
               SELECT p.id, p.slug, p.title, p.difficulty, p.url, p.tag
               FROM problems p
               LEFT JOIN users_problems up ON p.id = up.problem_id
               AND up.user_id = $2
               WHERE up.id IS NULL and difficulty = $1
               ORDER BY RANDOM()
               LIMIT 1
               """,
               difficulty,
               user_id
               )
           return row

    async def mark_problem_shown(self, user_id, problem_id):
        assert self._pool is not None
        async with self._pool.acquire() as conn:
            await conn.execute("""
            INSERT INTO users_problems (user_id, problem_id, status, given_at)
            VALUES ($1, $2, 'shown', NOW())
            """, user_id, problem_id
            )

    async def mark_problem_solved(self, user_id: int, problem_id: int):
        assert self._pool is not None
        async with self._pool.acquire() as conn:
            await conn.execute("""
            UPDATE users_problems SET status = 'solved', solved_at = NOW()
            WHERE user_id = $1 AND problem_id = $2
            """, user_id, problem_id)

    async def get_or_create_user_id(self, tg_id: int) -> int:
        assert self._pool is not None
        async with self._pool.acquire() as conn:
            row = await conn.fetchrow(
                """
                INSERT INTO users (tg_id)
                VALUES ($1)
                ON CONFLICT (tg_id) DO UPDATE
                    SET tg_id = EXCLUDED.tg_id
                RETURNING id
                """,
                tg_id,
            )
        return row["id"]

    async def get_user_stats(self, user_id: int):
        assert self._pool is not None
        async with self._pool.acquire() as conn:
            rows = await conn.fetch(
                """
                SELECT
                    p.difficulty,
                    COUNT(*) FILTER (WHERE up.status = 'shown')  AS shown_count,
                    COUNT(*) FILTER (WHERE up.status = 'solved') AS solved_count
                FROM users_problems up
                JOIN users u ON u.id = up.user_id
                JOIN problems p ON p.id = up.problem_id
                WHERE u.tg_id = $1
                GROUP BY p.difficulty
                ORDER BY p.difficulty;
                """,
                user_id,
            )
        return rows