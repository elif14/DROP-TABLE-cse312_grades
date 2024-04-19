if __name__ == '__main__':

   import asyncio

   from autobahn.asyncio.websocket import WebSocketServerFactory
   factory = WebSocketServerFactory()
   factory.protocol = MyServerProtocol

#    loop = asyncio.get_event_loop()
#    coro = loop.create_server(factory, '127.0.0.1', 9000)
#    server = loop.run_until_complete(coro)
   loop = asyncio.get_event_loop()
   coro = loop.create_connection(factory, '127.0.0.1', 9000)
   loop.run_until_complete(coro)
   loop.run_forever()
   loop.close()

#    try:
#       loop.run_forever()
#    except KeyboardInterrupt:
#       pass
#    finally:
#       server.close()
#       loop.close()


    


   def onOpen(self):
      self.sendMessage(u"Hello, world!".encode('utf8'))

   def onMessage(self, payload, isBinary):
      if isBinary:
         print("Binary message received: {0} bytes".format(len(payload)))
      else:
         print("Text message received: {0}".format(payload.decode('utf8')))