var EE = require('events').EventEmitter,
    assert = require('assert');

var oncemore = require('../oncemore');

var emitter = oncemore(new EE());

var once_called = false;
emitter.once('abc', 'def', 'ghi', function(arg1) {
  console.error('letters', arg1);
  assert.equal(arguments.length, 1);
  assert.equal(arg1, 'first');
  once_called = true;
});

var oncemore_called = false;
emitter.oncemore('abc', 'def', 'ghi', function(type, arg1) {
  console.error('emitted', type, arg1);
  assert.equal(arguments.length, 2);
  assert.equal(arg1, 'first');
  assert.equal(type, 'def');
  oncemore_called = true;
});

emitter.emit('def', 'first');
emitter.emit('abc', 'second');

emitter.on = function(ev, fn) {
  var res = EE.prototype.on.call(this, ev, fn);

  if (ev === 'def')
    this.emit('def', 'immediate');

  return res;
}

var oncemore_called2 = false;
emitter.oncemore(['abc', 'def', 'ghi'], function(type, arg1) {
  console.error('emitted', type, arg1);
  assert.equal(arguments.length, 2);
  assert.equal(arg1, 'immediate');
  assert.equal(type, 'def');
  oncemore_called2 = true;
});

emitter.emit('abc', 'late');

process.on('exit', function() {
  assert(once_called);
  assert(oncemore_called);
  assert(oncemore_called2);

  // check that no listeners remain
  assert(!emitter._events.abc);
  assert(!emitter._events.def);
  assert(!emitter._events.ghi);

  console.error('done!');
});
