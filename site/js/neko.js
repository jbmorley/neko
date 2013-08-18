/*
 * Copyright (c) 2013 Jason Barrie Morley.
 * 
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 * 
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 * 
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 */

$(document).ready(function(){

  var getStatus = function(identifier, icon) {
    var element = $('#' + identifier);
    if (element.length === 0) {
      element = createStatus(identifier, icon);
    }
    return element;
  };

  var createStatus = function(identifier, icon) {
    var i = $('<i />', {
      'class': icon
    });

    var item = $('<div />', {
      'id': identifier,
      'class': 'item'
    });

    item.append(i);
    $('#container').append(item);
    return item;
  };

  console.log("Beginning update...");
  $.getJSON('api', function(data) {
    $.each(data, function(index, value) {
      var status = getStatus(value['name'], value['icon']);
      var state = value['state'];
      if (state === 0) {
        status.addClass('red');
        status.removeClass('amber');
        status.removeClass('green');
      } else if (state === 1) {
        status.addClass('amber');
        status.removeClass('red');
        status.removeClass('green');
      } else if (state === 2) {
        status.addClass('green');
        status.removeClass('amber');
        status.removeClass('red');
      }
    });
  })
  .success(function() { console.log("Success"); })
  .error(function() { console.log("Error"); })
  .complete(function() { console.log("Complete"); });

});