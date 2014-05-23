import json
import collections
import re


__version__ = '0.1.0'
VERSION = tuple(map(int, __version__.split('.')))

__all__ = ['NotifyDict', 'NotifyList', 'watch', 'unwatch']


class NotifyBase(object):

	def __init__(self):
		self._listeners = {}  # Dict of listener lists, keyed by event

	def on(self, event, listener):
		if listener is not None:
			self._listeners.setdefault(event, []).append(listener)
		return self

	def _notify(self, type, name, path, value, oldvalue):
		for event, listeners in self._listeners.iteritems():
			try:
				type_filter, path_filter = event.split(' ', 1)
			except ValueError:
				type_filter, path_filter = event, ''
			if type != type_filter and type_filter != 'change':
				continue
			re_path = '.' + '.'.join([str(v) for v in path])
			path_filter = path_filter.replace('.', '\.').replace('[', '\.').replace(']', '') + '.*'
			if not re.search(path_filter, re_path):
				continue
			for listener in listeners:
				listener({
					'object': self,
					'type': type,
					'name': name,
					'path': path,
					'value': value,
					'oldvalue': oldvalue
				})

	def _listen(self, record):
		if isinstance(self, NotifyDict):
			subpath = self._dict.keys()[self._dict.values().index(record['object'])]
		elif isinstance(self, NotifyList):
			subpath = self._list.index(record['object'])
		record['path'].insert(0, subpath)
		self._notify(record['type'], record['name'], record['path'], record['value'], record['oldvalue'])

	def to_json(self, **options):
		return json.dumps(unwatch(self), **options)

	def path(self, path):
		return reduce(lambda d, k: d[k], path, self)


class NotifyDict(collections.MutableMapping, NotifyBase):

	def __init__(self, *args, **kwargs):
		super(NotifyDict, self).__init__()
		self._dict = dict()

	def __repr__(self):
		return repr(self._dict)

	def __len__(self):
		return len(self._dict)

	def __iter__(self):
		return iter(self._dict)

	def __getitem__(self, key):
		return self._dict[key]

	def __setitem__(self, key, value):
		oldvalue = self._dict[key] if key in self._dict else None
		self._dict[key] = watch(value, self._listen)
		self._notify('set', key, [key], value, oldvalue)

	def __delitem__(self, key):
		oldvalue = self._dict[key]
		del self._dict[key]
		self._notify('delete', key, [key], None, oldvalue)

	def to_dict(self):
		return unwatch(self)

	@staticmethod
	def from_dict(d):
		if not isinstance(d, dict):
			raise TypeError('You must pass a dict!')
		return watch(d)


class NotifyList(collections.MutableSequence, NotifyBase):

	def __init__(self):
		super(NotifyList, self).__init__()
		self._list = list()

	def __repr__(self):
		return repr(self._list)

	def __len__(self):
		return len(self._list)

	def __getitem__(self, index):
		return self._list[index]

	def __setitem__(self, index, value):
		oldvalue = self._list[index]
		self._list[index] = watch(value, self._listen)
		self._notify('set', index, [index], value, oldvalue)

	def __delitem__(self, index):
		oldvalue = self._list[index]
		del self._list[index]
		self._notify('delete', index, [index], None, oldvalue)

	def insert(self, index, value):
		self._list.insert(index, watch(value, self._listen))
		self._notify('insert', index, [index], value, None)

	def to_list(self):
		return unwatch(self)

	@staticmethod
	def from_list(l):
		if not isinstance(l, list):
			raise TypeError('You must pass a list!')
		return watch(l)


def watch(x, listener=None, event='change'):
	if isinstance(x, (NotifyDict, NotifyList)):
		return x.on(event, listener)
	elif isinstance(x, dict):
		n = NotifyDict()
		for k, v in dict.iteritems(x):
			n[k] = v
		return n.on(event, listener)
	elif isinstance(x, list):
		n = NotifyList()
		for v in x:
			n.append(v)
		return n.on(event, listener)
	else:
		return x

def unwatch(x):
	if isinstance(x, NotifyDict):
		x = x._dict
	elif isinstance(x, NotifyList):
		x = x._list
	if isinstance(x, dict):
		return dict((k, unwatch(v)) for k, v in x.iteritems())
	elif isinstance(x, list):
		return list(unwatch(v) for v in x)
	else:
		return x