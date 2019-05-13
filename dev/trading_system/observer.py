"""
Define a one-to-many dependency between objects so that when one object
changes state, all its dependents are notified and updatedautomatically.
"""

import abc
import json
from functools import reduce

from websocket import create_connection

from trading_system.models import AuctionParticipant


class Subject:
	"""
	Know its observers. Any number of Observer objects may observe a
	subject.
	Send a notification to its observers when its state changes.
	"""

	def __init__(self):
		self._observers = set()
		self._subject_state = None

	def attach(self, observer):
		observer._subject = self
		self._observers.add(observer)

	def detach(self, observer):
		observer._subject = None
		self._observers.discard(observer)

	def _notify(self):
		for observer in self._observers:
			observer.update(self._subject_state)

	@property
	def subject_state(self):
		return self._subject_state

	@subject_state.setter
	def subject_state(self, arg):
		self._subject_state = arg
		self._notify()


class Observer(metaclass=abc.ABCMeta):
	"""
	Define an updating interface for objects that should be notified of
	changes in a subject.
	"""

	def __init__(self):
		self._subject = None
		self._observer_state = None

	@abc.abstractmethod
	def update(self, arg):
		pass


class AuctionPrticipantObserver(Observer):
	"""
	Implement the Observer updating interface to keep its state
	consistent with the subject's.
	Store state that should stay consistent with the subject's.
	"""

	def __init__(self, participant):
		Observer.__init__(self)
		self._participant = participant

	def update(self, auction_id):
		ws = create_connection(self._participant.address)
		participants = list(AuctionParticipant.objects.filter(auction_id=auction_id))
		best_offer = reduce(lambda acc, curr: max(acc, curr.offer), participants, 0)
		if best_offer > self._participant.offer:
			ws.send(json.dumps({'message': 'Someone offered {} for this item.'.format(best_offer)+
			                               'You offer is no longer the best offer'}))


class AuctionSubject(Subject):
	def __init__(self, auction_id):
		Subject.__init__(self)
		self._auction_id = auction_id
		self._subject_state = self._auction_id
		obs = list(map(lambda ap: AuctionPrticipantObserver(ap),list(AuctionParticipant.objects.filter(auction_id=auction_id))))
		for o in obs:
			self.attach(o)
