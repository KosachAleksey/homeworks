import asyncio
import aiofiles  # Теперь это будет импортировать библиотеку, а не ваш файл
from datetime import datetime
import os

class AsyncLogger:
    def __init__(self, log_dir: str = "logs"):
        self.log_dir = log_dir
        os.makedirs(log_dir, exist_ok=True)
        self.log_file = f"{log_dir}/log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
    async def _write_log(self, level: str, message: str):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        log_entry = f"[{timestamp}] [{level}] {message}\n"
        
        async with aiofiles.open(self.log_file, mode='a') as f:
            await f.write(log_entry)
    
    async def info(self, message: str):
        await self._write_log("INFO", message)
    
    async def error(self, message: str):
        await self._write_log("ERROR", message)
    
    async def debug(self, message: str):
        await self._write_log("DEBUG", message)

class AsyncTaskQueue:
    def __init__(self):
        self.logger = AsyncLogger()
        self.queue = asyncio.Queue()
        self.is_running = False
    
    async def add_task(self, task: str):
        await self.queue.put(task)
        await self.logger.info(f"Task added: {task} (Queue size: {self.queue.qsize()})")
    
    async def process_task(self):
        self.is_running = True
        try:
            while not self.queue.empty():
                task = await self.queue.get()
                await self.logger.debug(f"Processing task: {task}")
                
                # Имитация обработки задачи
                await asyncio.sleep(1)
                
                await self.logger.info(f"Task completed: {task} (Remaining: {self.queue.qsize()})")
                self.queue.task_done()
        except Exception as e:
            await self.logger.error(f"Error processing task: {str(e)}")
        finally:
            self.is_running = False
            await self.logger.info("Queue processing stopped")
    
    async def shutdown(self):
        if not self.queue.empty():
            await self.logger.error("Shutdown called with non-empty queue!")
        await self.logger.info("Shutting down the task queue")

async def main():
    logger = AsyncLogger()
    await logger.info("Starting application")
    
    task_queue = AsyncTaskQueue()
    
    # Добавляем задачи
    for i in range(1, 6):
        await task_queue.add_task(f"Task-{i}")
    
    # Обрабатываем задачи
    processor = asyncio.create_task(task_queue.process_task())
    
    # Добавляем еще задач во время обработки
    await asyncio.sleep(2)
    for i in range(6, 9):
        await task_queue.add_task(f"Task-{i}")
    
    # Ждем завершения обработки
    await task_queue.queue.join()
    await task_queue.shutdown()
    
    await logger.info("Application finished")

if __name__ == "__main__":
    asyncio.run(main())
    