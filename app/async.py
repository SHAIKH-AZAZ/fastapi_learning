import time
from rich import print
import asyncio




async def endpoint(route: str)-> str:
    print(f">> handling {route}")

    # emualting database delay
    await asyncio.sleep(1) 
    print(f"<< response {route}")
    return route
    
    
# endpoint("")

async def server():
    # run tests request
    tests = (
        "GET/shipment?id=1",
        "PATH/shipment?id=4",
        "GET/shipment?id=3"
    )
    start = time.perf_counter()
    
    async with asyncio.TaskGroup() as task_group:
        tasks = [
            task_group.create_task(endpoint(route))
            for route in tests
            ]


    end = time.perf_counter()
    
    print(f"{end - start:.2f}")
    
    
asyncio.run(server())