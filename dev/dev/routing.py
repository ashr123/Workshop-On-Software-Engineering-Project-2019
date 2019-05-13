from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import store.routing
import trading_system.routing

application = ProtocolTypeRouter({
	# (http->django views is added by default)
	'websocket': AuthMiddlewareStack(
		URLRouter(
			trading_system.routing.websocket_urlpatterns
		)
	),
})
