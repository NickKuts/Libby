"use strict";

var fs = require('fs'),
    util = require('util'),
    Transform = require('stream').Transform || require('readable-stream/transform');

var oncemore = require('oncemore');

var exports = module.exports = TailStream;

TailStream.START_DELAY = 50; /* ms */

function TailStream(path, options) {
  if (!(this instanceof TailStream))
    return new TailStream(path, options);

  options = options || {};

  Transform.call(this, options);

  if (options.end !== undefined)
    throw new Error('"end" option is not supported');

  this.path = path;
  this.flags = 'r';
  this.fd = options.hasOwnProperty('fd') ? options.fd : null;
  this.autoClose = !!options.autoClose;

  this.closing = false;
  this.closed = false;

  this._offset = ~~options.start;
  this._handle = null;
  this._delay = TailStream.START_DELAY;

  this.poll();

  this.on('end', function() {
    if (this.autoClose) {
      this.destroy();
    }
  });
};
util.inherits(TailStream, Transform);

TailStream.prototype._transform = function _transform(chunk, encoding, done) {
  this._offset += chunk.length;
  return done(null, chunk);
};

TailStream.prototype.open = function() {
  var self = this;

  fs.open(this.path, this.flags, function(err, fd) {
    if (err) {
      if (self.autoClose)
        self.destroy();

      return self.emit('error', err);
    }

    self.fd = fd;
    self.emit('open', fd);
  });
};

TailStream.prototype.poll = function() {
  var self = this;

  if (this.fd)
    fs.fstat(this.fd, handleStat);
  else
    fs.stat(this.path, handleStat);

  var wasClosing = self.closing;

  function handleStat(err, stat) {
    if (!err && !stat.isFile())
      err = new Error('path does not point to a regular file');

    if (err) {
      if (err.code && err.code === 'ENOENT') {
        if (!self.fd)
          return doNextAction(); // keep looking

        return self.end();
      }

      return doNextAction();
    }

    // check if file has been deleted
    if (stat.nlink === 0)
      return self.end();

    if (!self.fd && !self.closed) {
      self.once('open', function () {
        self.fill(doNextAction);
      });
      return self.open();
    }

    if (stat.size > self._offset)
      return self.fill(doNextAction);

    doNextAction();
  }

  function doNextAction(err) {
    if (err) {
      if (self.autoClose)
        self.destroy();

      return self.emit('error', err);
    }

    if (wasClosing && !self.autoClose)
      return self.close(self.end.bind(self));

    self._delay = Math.min(1000, self._delay * 2);

    setTimeout(self.poll.bind(self), self._delay);
  }
};

TailStream.prototype.fill = function(done) {
  var self = this;

  this._delay = TailStream.START_DELAY;

  this._handle = oncemore(fs.createReadStream(this.path, {fd:this.fd, autoClose:false, start:this._offset}));
  this._handle.pipe(this, {end:false});
  this._handle.once('end', 'error', function(err) {
    self._handle = null;
    done(err);
  });
};

TailStream.prototype.destroy = function() {
  if (this.destroyed)
    return;
  this.destroyed = true;

  if (this.fd !== null)
    this.close();
};

TailStream.prototype.close = function(cb) {
  var self = this;
  if (cb)
    this.once('close', cb);
  if (this.closed || this.fd === null) {
    // TODO: move this, as open() is not guaranteed to be called
    if (this.fd === null) {
      this.once('open', close);
      return;
    }
    return process.nextTick(this.emit.bind(this, 'close'));
  }
  this.closed = true;
  close();

  function close(fd) {
    fs.close(fd || self.fd, function(er) {
      if (er)
        self.emit('error', er);
      else
        self.emit('close');
    });
    self.fd = null;
  }
};


// calling done signals that a final size check should be made, before ending the stream
TailStream.prototype.done = function() {
  this.closing = true;
  this._delay = TailStream.START_DELAY;
};

exports.createReadStream = function createReadStream(path, options) {
  return new TailStream(path, options);
};
