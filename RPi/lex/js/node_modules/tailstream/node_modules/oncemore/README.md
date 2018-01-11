# oncemore node.js module

Extend the `once()` method of any `EventEmitter` to allow a single listener to be attached to multiple events.
This is designed to simplify consumption of node streams, where you need to trigger an action "when it's done" by listening to both the `'end'` and `'error'` emits, but applicable to any event emitter.

## Setup

To prepare any emitter, wrap it in `oncemore()`.

    var EventEmitter = require('events').EventEmitter;
    var oncemore = require('oncemore');

    var emitter = oncemore(new EventEmitter());

## Usage

Basic example:

    emitter.once('end', 'error', function(err) {
      // do stuff
    });

Alternatively, if you need to know the triggered event:

    emitter.oncemore('end', 'error', 'timeout', function(type, err) {
      // do stuff
    });

### Limitations

Unlike regular `once` handlers, oncemore handlers are only designed to be removed by being triggered, and you must **not** use `removeListener(…)`. You can still use `removeAllListeners(…)`.

## Installation

    npm install oncemore

## Syntax

### emitter.once(event1[, event2[, …]]], listener)

Add a **one time** listener for the events. This listener is invoked only the next time any of the events are emitted, after which it is removed.

### emitter.oncemore(event1[, event2[, …]]], listener)

Similar to the updated `once` method, except that the first argument to the listener contains the type of the triggered event.

The event names can also be passed as a single `Array`.

#License
(BSD 2-Clause License)

Copyright (c) 2013, Gil Pedersen &lt;gpdev@gpost.dk&gt;  
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met: 

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer. 
2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution. 

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
