# from django.contrib.auth import get_
from channels.consumer import AsyncConsumer
from multiprocessing import Process, Value
from .slicer import SliceResearch
import asyncio, json, time

SlicerProcesses = {}

class UploadResearchConsumer(AsyncConsumer):
	async def websocket_connect(self, event):
		await self.send({
			"type": "websocket.accept"
		})

	async def websocket_receive(self, event):
		text = event.get("text", None)
		if text is not None:
			data = json.loads(text)
			filename = data.get("filename", None)

			myID = self.scope["session"]["id"]

			if filename == None:
				return
			if myID not in SlicerProcesses.keys():
				progress = Value('d', 0.0)
				status = Value('i', 1)
				process = Process(target=SliceResearch, args=(filename, status, progress))
				process.start()

				SlicerProcesses[myID] = {
					"process": process,
					"status": status, 
					"progress": progress,
				}

			if SlicerProcesses[myID]["process"].is_alive():
				status = SlicerProcesses[myID]["status"].value
			
				response = {
					"progress": SlicerProcesses[myID]["progress"].value,
					"status": status,
				}

				await self.send({
					"type": "websocket.send",
					"text": json.dumps(response),
				}) 
			else:
				response = {
					"progress": 0,
					"status": 5,
				}

				await self.send({
					"type": "websocket.send",
					"text": json.dumps(response),
				}) 

				del SlicerProcesses[myID]


	async def websocket_disconnect(self, event):
		print("disconnected", event)