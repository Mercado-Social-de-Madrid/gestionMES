(function webpackUniversalModuleDefinition(root, factory) {
	if(typeof exports === 'object' && typeof module === 'object')
		module.exports = factory();
	else if(typeof define === 'function' && define.amd)
		define([], factory);
	else if(typeof exports === 'object')
		exports["TimePicker"] = factory();
	else
		root["TimePicker"] = factory();
})(this, function() {
return /******/ (function(modules) { // webpackBootstrap
/******/ 	// The module cache
/******/ 	var installedModules = {};
/******/
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/
/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId]) {
/******/ 			return installedModules[moduleId].exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			i: moduleId,
/******/ 			l: false,
/******/ 			exports: {}
/******/ 		};
/******/
/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/
/******/ 		// Flag the module as loaded
/******/ 		module.l = true;
/******/
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/
/******/
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;
/******/
/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;
/******/
/******/ 	// define getter function for harmony exports
/******/ 	__webpack_require__.d = function(exports, name, getter) {
/******/ 		if(!__webpack_require__.o(exports, name)) {
/******/ 			Object.defineProperty(exports, name, {
/******/ 				configurable: false,
/******/ 				enumerable: true,
/******/ 				get: getter
/******/ 			});
/******/ 		}
/******/ 	};
/******/
/******/ 	// getDefaultExport function for compatibility with non-harmony modules
/******/ 	__webpack_require__.n = function(module) {
/******/ 		var getter = module && module.__esModule ?
/******/ 			function getDefault() { return module['default']; } :
/******/ 			function getModuleExports() { return module; };
/******/ 		__webpack_require__.d(getter, 'a', getter);
/******/ 		return getter;
/******/ 	};
/******/
/******/ 	// Object.prototype.hasOwnProperty.call
/******/ 	__webpack_require__.o = function(object, property) { return Object.prototype.hasOwnProperty.call(object, property); };
/******/
/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "";
/******/
/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(__webpack_require__.s = 0);
/******/ })
/************************************************************************/
/******/ ([
/* 0 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.TimePicker = undefined;

var _timepicker = __webpack_require__(1);

var _timepicker2 = _interopRequireDefault(_timepicker);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

exports.TimePicker = _timepicker2.default;

/***/ }),
/* 1 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
  value: true
});

var _slicedToArray = function () { function sliceIterator(arr, i) { var _arr = []; var _n = true; var _d = false; var _e = undefined; try { for (var _i = arr[Symbol.iterator](), _s; !(_n = (_s = _i.next()).done); _n = true) { _arr.push(_s.value); if (i && _arr.length === i) break; } } catch (err) { _d = true; _e = err; } finally { try { if (!_n && _i["return"]) _i["return"](); } finally { if (_d) throw _e; } } return _arr; } return function (arr, i) { if (Array.isArray(arr)) { return arr; } else if (Symbol.iterator in Object(arr)) { return sliceIterator(arr, i); } else { throw new TypeError("Invalid attempt to destructure non-iterable instance"); } }; }();

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

var _template = __webpack_require__(2);

var _template2 = _interopRequireDefault(_template);

var _assign = __webpack_require__(3);

var _assign2 = _interopRequireDefault(_assign);

var _events = __webpack_require__(4);

var _events2 = _interopRequireDefault(_events);

__webpack_require__(5);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

/**
 * @class TimePicker
 *
 * @prop {string} template - TimePicker template
 * @prop {object} defaultOptions - Default config options
 * @prop {string} defaultOptions.timeFormat - 12 or 24 hour format ['standard', 'military']
 * @prop {bool} defaultOptions.autoNext - Auto-next on time element select
 * @prop {object} cachedEls - Cached elements in template
 * @prop {HTMLElement} cachedEls.body - document.body
 * @prop {HTMLElement} cachedEls.overlay - Overlay element ('.mtp-overlay')[0]
 * @prop {HTMLElement} cachedEls.wrapper - Wrapper element ('.mtp-wrapper')[0]
 * @prop {HTMLElement} cachedEls.picker - Selection elements wrapper ('.mtp-picker')[0]
 * @prop {HTMLElement} cachedEls.meridiem - Meridiem selection elements wrapper ('.mtp-meridiem')[0]
 * @prop {HTMLCollection} cachedEls.meridiemSpans - Meridiem selection elements meridiem('span')
 * @prop {HTMLElement} cachedEls.displayHours - Selected hour display element ('.mtp-display__hours')[0]
 * @prop {HTMLElement} cachedEls.displayMinutes - Selected minutes display element ('.mtp-display__minutes')[0]
 * @prop {HTMLElement} cachedEls.displayMerdiem - Selected meridiem display element ('.mtp-display__meridiem')[0]
 * @prop {HTMLElement} cachedEls.buttonCancel - Cancel button element ('.mtp-actions__cancel')[0]
 * @prop {HTMLElement} cachedEls.buttonBack - Back button element ('.mtp-actions__back')[0]
 * @prop {HTMLElement} cachedEls.buttonNext - Next button element ('.mtp-actions__next')[0]
 * @prop {HTMLElement} cachedEls.buttonFinish - Finish button element ('.mtp-actions__finish')[0]
 * @prop {HTMLElement} cachedEls.clockHours - Hour elements display wrapper ('.mtp-clock__hours')[0]
 * @prop {HTMLElement} cachedEls.clockMinutes - Minute elements display wrapper ('.mtp-clock__minutes')[0]
 * @prop {HTMLElement} cachedEls.clockMilitaryHours - Military hour elements display wrapper ('.mtp_clock__hours--military')[0]
 * @prop {HTMLElement} cachedEls.clockHand - Clock hand display ('.mtp-clock__hand')[0]
 * @prop {HTMLCollection} cachedEls.clockHoursLi - Hour list elements clockHours('li')
 * @prop {HTMLCollection} cachedEls.clockMinutesLi - Minute list elements clockMinutes('li')
 * @prop {HTMLCollection} cachedEls.clockMilitaryHoursLi - Military Hour li elements clockMilitaryHours('li')
 */
var TimePicker = function () {

  /**
     * Initialize new TimePicker instance
     *
     * @return {TimePicker} New TimePicker instance
     */
  function TimePicker() {
    _classCallCheck(this, TimePicker);

    this.template = _template2.default;
    this.defaultOptions = {
      timeFormat: 'standard',
      autoNext: false
    };
    this.cachedEls = {};

    this.events = new _events2.default();

    this.setupTemplate();

    this.cachedEls.body = document.body;
    var _cachedEls$body$getEl = this.cachedEls.body.getElementsByClassName('mtp-overlay');

    var _cachedEls$body$getEl2 = _slicedToArray(_cachedEls$body$getEl, 1);

    this.cachedEls.overlay = _cachedEls$body$getEl2[0];

    var _cachedEls$overlay$ge = this.cachedEls.overlay.getElementsByClassName('mtp-wrapper');

    var _cachedEls$overlay$ge2 = _slicedToArray(_cachedEls$overlay$ge, 1);

    this.cachedEls.wrapper = _cachedEls$overlay$ge2[0];

    var _cachedEls$wrapper$ge = this.cachedEls.wrapper.getElementsByClassName('mtp-picker');

    var _cachedEls$wrapper$ge2 = _slicedToArray(_cachedEls$wrapper$ge, 1);

    this.cachedEls.picker = _cachedEls$wrapper$ge2[0];

    var _cachedEls$wrapper$ge3 = this.cachedEls.wrapper.getElementsByClassName('mtp-meridiem');

    var _cachedEls$wrapper$ge4 = _slicedToArray(_cachedEls$wrapper$ge3, 1);

    this.cachedEls.meridiem = _cachedEls$wrapper$ge4[0];

    this.cachedEls.meridiemSpans = this.cachedEls.meridiem.getElementsByTagName('span');
    var _cachedEls$wrapper$ge5 = this.cachedEls.wrapper.getElementsByClassName('mtp-display__hours');

    var _cachedEls$wrapper$ge6 = _slicedToArray(_cachedEls$wrapper$ge5, 1);

    this.cachedEls.displayHours = _cachedEls$wrapper$ge6[0];

    var _cachedEls$wrapper$ge7 = this.cachedEls.wrapper.getElementsByClassName('mtp-display__minutes');

    var _cachedEls$wrapper$ge8 = _slicedToArray(_cachedEls$wrapper$ge7, 1);

    this.cachedEls.displayMinutes = _cachedEls$wrapper$ge8[0];

    var _cachedEls$wrapper$ge9 = this.cachedEls.wrapper.getElementsByClassName('mtp-display__meridiem');

    var _cachedEls$wrapper$ge10 = _slicedToArray(_cachedEls$wrapper$ge9, 1);

    this.cachedEls.displayMeridiem = _cachedEls$wrapper$ge10[0];

    var _cachedEls$picker$get = this.cachedEls.picker.getElementsByClassName('mtp-actions__cancel');

    var _cachedEls$picker$get2 = _slicedToArray(_cachedEls$picker$get, 1);

    this.cachedEls.buttonCancel = _cachedEls$picker$get2[0];

    var _cachedEls$picker$get3 = this.cachedEls.picker.getElementsByClassName('mtp-actions__back');

    var _cachedEls$picker$get4 = _slicedToArray(_cachedEls$picker$get3, 1);

    this.cachedEls.buttonBack = _cachedEls$picker$get4[0];

    var _cachedEls$picker$get5 = this.cachedEls.picker.getElementsByClassName('mtp-actions__next');

    var _cachedEls$picker$get6 = _slicedToArray(_cachedEls$picker$get5, 1);

    this.cachedEls.buttonNext = _cachedEls$picker$get6[0];

    var _cachedEls$picker$get7 = this.cachedEls.picker.getElementsByClassName('mtp-actions__finish');

    var _cachedEls$picker$get8 = _slicedToArray(_cachedEls$picker$get7, 1);

    this.cachedEls.buttonFinish = _cachedEls$picker$get8[0];

    var _cachedEls$picker$get9 = this.cachedEls.picker.getElementsByClassName('mtp-clock__hours');

    var _cachedEls$picker$get10 = _slicedToArray(_cachedEls$picker$get9, 1);

    this.cachedEls.clockHours = _cachedEls$picker$get10[0];

    var _cachedEls$picker$get11 = this.cachedEls.picker.getElementsByClassName('mtp-clock__minutes');

    var _cachedEls$picker$get12 = _slicedToArray(_cachedEls$picker$get11, 1);

    this.cachedEls.clockMinutes = _cachedEls$picker$get12[0];

    var _cachedEls$picker$get13 = this.cachedEls.picker.getElementsByClassName('mtp-clock__hours-military');

    var _cachedEls$picker$get14 = _slicedToArray(_cachedEls$picker$get13, 1);

    this.cachedEls.clockMilitaryHours = _cachedEls$picker$get14[0];

    var _cachedEls$picker$get15 = this.cachedEls.picker.getElementsByClassName('mtp-clock__hand');

    var _cachedEls$picker$get16 = _slicedToArray(_cachedEls$picker$get15, 1);

    this.cachedEls.clockHand = _cachedEls$picker$get16[0];

    this.cachedEls.clockHoursLi = this.cachedEls.clockHours.getElementsByTagName('li');
    this.cachedEls.clockMinutesLi = this.cachedEls.clockMinutes.getElementsByTagName('li');
    this.cachedEls.clockMilitaryHoursLi = this.cachedEls.clockMilitaryHours.getElementsByTagName('li');

    this.setEvents();
  }

  /**
     * Bind event to the input element to open when `focus` event is events.triggered
     *
     * @param {string|HTMLElement} inputEl Selector element to be queried or existing HTMLElement
     * @param {object} options Options to merged with defaults and set to input element object
     * @return {void}
     */


  _createClass(TimePicker, [{
    key: 'bindInput',
    value: function bindInput(inputEl) {
      var _this = this;

      var options = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : {};

      var element = inputEl instanceof HTMLElement ? inputEl : document.querySelector(inputEl);

      element.mtpOptions = (0, _assign2.default)({}, this.defaultOptions, options);
      element.addEventListener('focus', function (event) {
        return _this.showEvent(event);
      });
    }

    /**
       * Open picker with the input provided in context without binding events
       *
       * @param {string|HTMLElement} inputEl Selector element to be queried or existing HTMLElement
       * @param {object} options Options to merged with defaults and set to input element object
       * @return {void}
       */

  }, {
    key: 'openOnInput',
    value: function openOnInput(inputEl) {
      var options = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : {};

      this.inputEl = inputEl instanceof HTMLElement ? inputEl : document.querySelector(inputEl);
      this.inputEl.mtpOptions = (0, _assign2.default)({}, this.defaultOptions, options);
      this.show();
    }

    /**
       * Setup the template in DOM if not already
       *
       * @return {void}
       */

  }, {
    key: 'setupTemplate',
    value: function setupTemplate() {
      if (!this.isTemplateInDOM()) {
        document.body.insertAdjacentHTML('beforeend', _template2.default);
      }
    }

    /**
       * Set the events on picker elements
       *
       * @return {void}
       */

  }, {
    key: 'setEvents',
    value: function setEvents() {
      var _this2 = this;

      if (!this.hasSetEvents()) {
        // close
        this.cachedEls.overlay.addEventListener('click', function (event) {
          return _this2.hideEvent(event);
        });

        this.cachedEls.buttonCancel.addEventListener('click', function (event) {
          return _this2.hideEvent(event);
        });
        this.cachedEls.buttonNext.addEventListener('click', function () {
          return _this2.showMinutes();
        });
        this.cachedEls.buttonBack.addEventListener('click', function () {
          return _this2.showHours();
        });
        this.cachedEls.buttonFinish.addEventListener('click', function () {
          return _this2.finish();
        })

        // meridiem select events
        ;[].forEach.call(this.cachedEls.meridiemSpans, function (span) {
          span.addEventListener('click', function (event) {
            return _this2.meridiemSelectEvent(event);
          });
        })

        // time select events
        ;[].forEach.call(this.cachedEls.clockHoursLi, function (hour) {
          hour.addEventListener('click', function (event) {
            _this2.hourSelectEvent(event, _this2.cachedEls.clockHours, _this2.cachedEls.clockHoursLi);
          });
        });[].forEach.call(this.cachedEls.clockMilitaryHoursLi, function (hour) {
          hour.addEventListener('click', function (event) {
            _this2.hourSelectEvent(event, _this2.cachedEls.clockMilitaryHours, _this2.cachedEls.clockMilitaryHoursLi);
          });
        });[].forEach.call(this.cachedEls.clockMinutesLi, function (minute) {
          minute.addEventListener('click', function (event) {
            _this2.minuteSelectEvent(event, _this2.cachedEls.clockMinutes, _this2.cachedEls.clockMinutesLi);
          });
        });

        this.cachedEls.wrapper.classList.add('mtp-events-set');
      }
    }

    /**
       * Show the picker in the DOM
       *
       * @return {void}
       */

  }, {
    key: 'show',
    value: function show() {
      var isMilitaryFormat = this.isMilitaryFormat();

      // blur input to prevent onscreen keyboard from displaying (mobile hack)
      this.inputEl.blur();
      this.toggleHoursVisible(true, isMilitaryFormat);
      this.toggleMinutesVisible();
      this.setDisplayTime({
        hours: isMilitaryFormat ? '00' : '12',
        minutes: '0'
      });

      this.cachedEls.body.style.overflow = 'hidden';
      this.cachedEls.displayMeridiem.style.display = isMilitaryFormat ? 'none' : 'inline';
      this.cachedEls.meridiem.style.display = isMilitaryFormat ? 'none' : 'block';
      this.cachedEls.overlay.style.display = 'block';
      this.cachedEls.clockHand.style.height = isMilitaryFormat ? '90px' : '105px';

      this.events.trigger('show');
    }

    /**
       * Event handle for input focus
       *
       * @param {Event} event Event object passed from listener
       * @return {void}
       */

  }, {
    key: 'showEvent',
    value: function showEvent(event) {
      this.inputEl = event.target;
      this.show();
    }

    /**
       * Hide the picker in the DOM
       *
       * @return {void}
       */

  }, {
    key: 'hide',
    value: function hide() {
      this.cachedEls.overlay.style.display = 'none';
      this.cachedEls.body.style.overflow = '';

      this.inputEl.dispatchEvent(new Event('blur'));
      this.resetState();
      this.events.trigger('hide');
    }

    /**
       * Hide the picker element on the page
       *
       * @param {Event} event Event object passed from event listener callback
       * @return {void}
       */

  }, {
    key: 'hideEvent',
    value: function hideEvent(event) {
      event.stopPropagation();

      // only allow event based close if event.target contains one of these classes
      // hack to prevent overlay close event from events.triggering on all elements because
      // they are children of overlay
      var allowedClasses = ['mtp-overlay', 'mtp-actions__cancel'];
      var classList = event.target.classList;

      var isAllowed = allowedClasses.some(function (allowedClass) {
        return classList.contains(allowedClass);
      });

      if (isAllowed) {
        this.hide();
      }
    }

    /**
       * Reset picker state to defaults
       *
       * @return {void}
       */

  }, {
    key: 'resetState',
    value: function resetState() {
      this.currentStep = 0;
      this.toggleHoursVisible(true, this.isMilitaryFormat());
      this.toggleMinutesVisible();
      this.cachedEls.clockHoursLi[0].dispatchEvent(new Event('click'));
      this.cachedEls.clockMinutesLi[0].dispatchEvent(new Event('click'));
      this.cachedEls.clockMilitaryHoursLi[0].dispatchEvent(new Event('click'));
      this.cachedEls.meridiemSpans[0].dispatchEvent(new Event('click'));
    }

    /**
       * Set the displayed time, which will be used to fill input value on completion
       *
       * @param {number|string} hours: Hour display time,
       * @param {number|string} minutes: Minute display time
       * @return {void}
       */

  }, {
    key: 'setDisplayTime',
    value: function setDisplayTime(_ref) {
      var hours = _ref.hours,
          minutes = _ref.minutes;

      if (hours) {
        // .trim() is not allowed if hours is not recognized as a string,
        if (typeof hours === 'string' || hours instanceof String) {
          this.cachedEls.displayHours.innerHTML = hours.trim();
        } else {
          this.cachedEls.displayHours.innerHTML = hours;
        }
      }
      if (minutes) {
        var min = minutes < 10 ? '0' + minutes : minutes;

        // .trim() is not allowed if min is not recognized as a string,
        // ... sometimes (in Safari and Chrome) it is an untrimmable number
        if (typeof min === 'string' || min instanceof String) {
          this.cachedEls.displayMinutes.innerHTML = min.trim();
        } else {
          this.cachedEls.displayMinutes.innerHTML = min;
        }
      }

      var numericHour = parseInt(hours);
      var numericMinute = parseInt(minutes);
    }

    /**
       * Rotate the hand element to selected time
       *
       * @param {number} nodeIndex Index of active element
       * @param {number} increment Degree increment elements are on
       * @return {void}
       */

  }, {
    key: 'rotateHand',
    value: function rotateHand() {
      var nodeIndex = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : 9;
      var increment = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : 30;

      // 0 index is 180 degress behind 0 deg
      var rotateDeg = nodeIndex * increment - 180;
      var styleVal = 'rotate(' + rotateDeg + 'deg)';

      this.cachedEls.clockHand.style.transform = styleVal;
      this.cachedEls.clockHand.style['-webkit-transform'] = styleVal;
      this.cachedEls.clockHand.style['-ms-transform'] = styleVal;
    }
  }, {
    key: 'showHours',
    value: function showHours() {
      var isMilitaryFormat = this.isMilitaryFormat();
      var hourEls = isMilitaryFormat ? this.cachedEls.clockMilitaryHoursLi : this.cachedEls.clockHoursLi;

      this.toggleHoursVisible(true, isMilitaryFormat);
      this.toggleMinutesVisible();
      this.rotateHand(this.getActiveIndex(hourEls));
    }
  }, {
    key: 'showMinutes',
    value: function showMinutes() {
      var minuteEls = this.cachedEls.clockMinutesLi;

      this.toggleHoursVisible();
      this.toggleMinutesVisible(true);
      this.rotateHand(this.getActiveIndex(minuteEls), 6);
      this.cachedEls.clockHand.style.height = '115px';
    }
  }, {
    key: 'finish',
    value: function finish() {
      this.timeSelected();
      this.hide();
    }

    /**
       * Toggle hour (both military and standard) clock visiblity in DOM
       *
       * @param {boolean} isVisible Is clock face toggled visible or hidden
       * @param {boolean} isMilitaryFormat Is using military hour format
       * @return {void}
       */

  }, {
    key: 'toggleHoursVisible',
    value: function toggleHoursVisible() {
      var isVisible = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : false;
      var isMilitaryFormat = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : false;

      this.cachedEls.clockHours.style.display = isVisible && !isMilitaryFormat ? 'block' : 'none';
      this.cachedEls.clockMilitaryHours.style.display = isVisible && isMilitaryFormat ? 'block' : 'none';
      this.cachedEls.buttonNext.style.display = !isVisible ? 'inline-block' : 'none';
    }

    /**
       * Toggle minute clock visiblity in DOM
       *
       * @param {boolean} isVisible Is clock face toggled visible or hidden
       * @return {void}
       */

  }, {
    key: 'toggleMinutesVisible',
    value: function toggleMinutesVisible() {
      var isVisible = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : false;

      this.cachedEls.clockMinutes.style.display = isVisible ? 'block' : 'none';
      this.cachedEls.buttonBack.style.display = isVisible ? 'inline-block' : 'none';
      this.cachedEls.buttonNext.style.display = !isVisible ? 'inline-block' : 'none';
      this.cachedEls.buttonFinish.style.display = isVisible ? 'inline-block' : 'none';
    }

    /**
       * Get the active time element index
       *
       * @param {HTMLCollection} timeEls Collection of time elements to find active in
       * @return {number} Active element index
       */

  }, {
    key: 'getActiveIndex',
    value: function getActiveIndex(timeEls) {
      var activeIndex = 0;[].some.call(timeEls, function (timeEl, index) {
        if (timeEl.classList.contains('mtp-clock--active')) {
          activeIndex = index;

          return true;
        }

        return false;
      });

      return activeIndex;
    }

    /**
       * Set selected time to input element
       *
       * @return {void}
       */

  }, {
    key: 'timeSelected',
    value: function timeSelected() {
      var hours = this.cachedEls.displayHours.innerHTML;
      var minutes = this.cachedEls.displayMinutes.innerHTML;
      var meridiem = this.isMilitaryFormat() ? '' : this.cachedEls.displayMeridiem.innerHTML;
      var timeValue = hours + ':' + minutes + ' ' + meridiem;

      this.inputEl.value = timeValue.trim();
      this.inputEl.dispatchEvent(new Event('input'));
      this.events.trigger('timeSelected', {
        hours: hours,
        minutes: minutes,
        meridiem: meridiem,
        value: timeValue
      });
    }

    /**
       * Set active clock face element
       *
       * @param {Element} containerEl New active elements .parentNode
       * @param {Element} activeEl Element to set active
       * @return {void}
       */

  }, {
    key: 'setActiveEl',
    value: function setActiveEl(containerEl, activeEl) {
      var activeClassName = 'mtp-clock--active';
      var currentActive = containerEl.getElementsByClassName(activeClassName)[0];

      currentActive.classList.remove(activeClassName);
      activeEl.classList.add(activeClassName);
    }

    /**
       * Meridiem select event handler
       *
       * @param {Event} event Event object passed from listener
       * @return {void}
       */

  }, {
    key: 'meridiemSelectEvent',
    value: function meridiemSelectEvent(event) {
      var activeClassName = 'mtp-clock--active';
      var element = event.target;
      var currentActive = this.cachedEls.meridiem.getElementsByClassName(activeClassName)[0];
      var value = element.innerHTML;

      if (!currentActive.isEqualNode(element)) {
        currentActive.classList.remove(activeClassName);
        element.classList.add(activeClassName);
        this.cachedEls.displayMeridiem.innerHTML = value;
      }
    }

    /**
       * Hour select event handler
       *
       * @param {Event} event Event object passed from listener
       * @param {HTMLElement} containerEl Element containing time list elements
       * @param {HTMLCollection} listEls Collection of list elements
       * @return {void}
       */

  }, {
    key: 'hourSelectEvent',
    value: function hourSelectEvent(event, containerEl, listEls) {
      event.stopPropagation();

      var newActive = event.target;
      var parentEl = newActive.parentElement;
      var isInner = parentEl.classList.contains('mtp-clock__hours--inner');

      this.cachedEls.clockHand.style.height = isInner ? '90px' : '105px';
      this.setActiveEl(containerEl, newActive);

      var activeIndex = this.getActiveIndex(listEls);

      this.setDisplayTime({ hours: newActive.innerHTML });
      this.rotateHand(activeIndex);
      this.events.trigger('hourSelected');
    }

    /**
       * Hour select event handler
       *
       * @param {Event} event Event object passed from listener
       * @param {HTMLElement} containerEl Element containing time list elements
       * @param {HTMLCollection} listEls Collection of list elements
       * @return {void}
       */

  }, {
    key: 'minuteSelectEvent',
    value: function minuteSelectEvent(event, containerEl, listEls) {
      event.stopPropagation();

      var newActive = event.target;

      this.setActiveEl(containerEl, newActive);

      var activeIndex = this.getActiveIndex(listEls);

      this.setDisplayTime({ minutes: activeIndex });
      this.rotateHand(activeIndex, 6);
      this.events.trigger('minuteSelected');
    }

    /**
       * Check if picker set to military time mode
       *
       * @return {boolean} Is in military time mode
       */

  }, {
    key: 'isMilitaryFormat',
    value: function isMilitaryFormat() {
      return this.inputEl.mtpOptions.timeFormat === 'military';
    }

    /**
       * Check if picker object has already set events on picker elements
       *
       * @return {boolean} Has events been set on picker elements
       */

  }, {
    key: 'hasSetEvents',
    value: function hasSetEvents() {
      return this.cachedEls.wrapper.classList.contains('mtp-events-set');
    }

    /**
       * Check if template has already been appended to DOM
       *
       * @return {boolean} Is template in DOM
       */

  }, {
    key: 'isTemplateInDOM',
    value: function isTemplateInDOM() {
      return Boolean(document.getElementsByClassName('mtp-overlay')[0]);
    }
  }]);

  return TimePicker;
}();

exports.default = TimePicker;

/***/ }),
/* 2 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
    value: true
});
var template = "\n<div class=\"mtp-overlay\" style=\"display:none\">\n    <div class=\"mtp-wrapper\">\n        <div class=\"mtp-display\">\n            <span class=\"mtp-display__hours\">12</span>:<span class=\"mtp-display__minutes\">00</span>\n            <span class=\"mtp-display__meridiem\">am</span>\n        </div><!-- END .mtp-display -->\n        <div class=\"mtp-picker\">\n            <div class=\"mtp-meridiem\">\n                <span class=\"mtp-clock--active\">am</span>\n                <span>pm</span>\n            </div><!-- END .mtp-meridiem -->\n            <div class=\"mtp-clock\">\n                <div class=\"mtp-clock__center\"></div>\n                <div class=\"mtp-clock__hand\"></div>\n                <ul class=\"mtp-clock__time mtp-clock__outer mtp-clock__hours\" style=\"display:none\">\n                    <li class=\"mtp-clock--active\">12</li>\n                    <li>1</li>\n                    <li>2</li>\n                    <li>3</li>\n                    <li>4</li>\n                    <li>5</li>\n                    <li>6</li>\n                    <li>7</li>\n                    <li>8</li>\n                    <li>9</li>\n                    <li>10</li>\n                    <li>11</li>\n                </ul>\n                <ul class=\"mtp-clock__time mtp-clock__outer mtp-clock__minutes\" style=\"display:none\">\n                    <li class=\"mtp-clock--active\">0</li>\n                    <li>&middot;</li>\n                    <li>&middot;</li>\n                    <li>&middot;</li>\n                    <li>&middot;</li>\n                    <li>5</li>\n                    <li>&middot;</li>\n                    <li>&middot;</li>\n                    <li>&middot;</li>\n                    <li>&middot;</li>\n                    <li>10</li>\n                    <li>&middot;</li>\n                    <li>&middot;</li>\n                    <li>&middot;</li>\n                    <li>&middot;</li>\n                    <li>15</li>\n                    <li>&middot;</li>\n                    <li>&middot;</li>\n                    <li>&middot;</li>\n                    <li>&middot;</li>\n                    <li>20</li>\n                    <li>&middot;</li>\n                    <li>&middot;</li>\n                    <li>&middot;</li>\n                    <li>&middot;</li>\n                    <li>25</li>\n                    <li>&middot;</li>\n                    <li>&middot;</li>\n                    <li>&middot;</li>\n                    <li>&middot;</li>\n                    <li>30</li>\n                    <li>&middot;</li>\n                    <li>&middot;</li>\n                    <li>&middot;</li>\n                    <li>&middot;</li>\n                    <li>35</li>\n                    <li>&middot;</li>\n                    <li>&middot;</li>\n                    <li>&middot;</li>\n                    <li>&middot;</li>\n                    <li>40</li>\n                    <li>&middot;</li>\n                    <li>&middot;</li>\n                    <li>&middot;</li>\n                    <li>&middot;</li>\n                    <li>45</li>\n                    <li>&middot;</li>\n                    <li>&middot;</li>\n                    <li>&middot;</li>\n                    <li>&middot;</li>\n                    <li>50</li>\n                    <li>&middot;</li>\n                    <li>&middot;</li>\n                    <li>&middot;</li>\n                    <li>&middot;</li>\n                    <li>55</li>\n                    <li>&middot;</li>\n                    <li>&middot;</li>\n                    <li>&middot;</li>\n                    <li>&middot;</li>\n                </ul>\n                <ul class=\"mtp-clock__time mtp-clock__hours-military\" style=\"display:none\">\n                    <div class=\"mtp-clock__hours--inner\">\n                        <li class=\"mtp-clock--active\">00</li>\n                        <li>13</li>\n                        <li>14</li>\n                        <li>15</li>\n                        <li>16</li>\n                        <li>17</li>\n                        <li>18</li>\n                        <li>19</li>\n                        <li>20</li>\n                        <li>21</li>\n                        <li>22</li>\n                        <li>23</li>\n                    </div>\n                    <div class=\"mtp-clock__hours\">\n                        <li>12</li>\n                        <li>1</li>\n                        <li>2</li>\n                        <li>3</li>\n                        <li>4</li>\n                        <li>5</li>\n                        <li>6</li>\n                        <li>7</li>\n                        <li>8</li>\n                        <li>9</li>\n                        <li>10</li>\n                        <li>11</li>\n                    </div>\n                </ul>\n            </div><!-- END .mtp-clock -->\n            <div class=\"mtp-actions\">\n                <button type=\"button\" class=\"mtp-actions__button mtp-actions__cancel\">Cancelar</button>\n                <button type=\"button\" class=\"mtp-actions__button mtp-actions__back\" style=\"display:none\">Atrás</button>\n                <button type=\"button\" class=\"mtp-actions__button mtp-actions__next\">Siguiente</button>\n                <button type=\"button\" class=\"mtp-actions__button mtp-actions__finish\" style=\"display:none\">Aceptar</button>\n            </div><!-- END .mtp-actions -->\n        </div><!-- END .mtp-picker -->\n    </div><!-- END .mtp-wrapper -->\n</div><!-- END .mtp-overlay -->\n";

exports.default = template;

/***/ }),
/* 3 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
  value: true
});
/* eslint-disable no-continue */
/**
 * Object.assign polyfill
 *
 * @param {object} target Target object to merge properties onto
 * @param {...object} sources  Source object to merge properties from
 * @return {object} Target object with merged properties
 */
function assign(target) {
  if (target === 'undefined' || target === null) {
    throw new TypeError('Cannot convert first argument to object');
  }

  var to = Object(target);

  for (var inc = 0; inc < (arguments.length <= 1 ? 0 : arguments.length - 1); inc += 1) {
    var nextSource = arguments.length <= inc + 1 ? undefined : arguments[inc + 1];

    if (nextSource === 'undefined' || nextSource === null) {
      continue;
    }

    nextSource = Object(nextSource);

    var keysArray = Object.keys(nextSource);

    for (var nextIndex = 0, len = keysArray.length; nextIndex < len; nextIndex += 1) {
      var nextKey = keysArray[nextIndex];
      var desc = Object.getOwnPropertyDescriptor(nextSource, nextKey);

      if (desc !== 'undefined' && desc.enumerable) {
        to[nextKey] = nextSource[nextKey];
      }
    }
  }

  return to;
}

exports.default = assign;

/***/ }),
/* 4 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
  value: true
});

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

/**
 * @class Events
 *
 * @prop {object.<string,function>} events - Hash table of events and their assigned handler callbacks
 */
var Events = function () {
  function Events() {
    _classCallCheck(this, Events);

    this.events = {};
  }

  _createClass(Events, [{
    key: "on",


    /**
       * Set handler on event
       *
       * @param {string} event - Event name to set handler to
       * @param {func} handler - Handler function callback
       * @return {void}
       */
    value: function on(event, handler) {
      if (!this.events[event]) {
        this.events[event] = [];
      }

      this.events[event].push(handler);
    }

    /**
       * Remove all event handler for the given event
       *
       * @param {string} event - Event name to remove handler from
       * @return {void}
       */

  }, {
    key: "off",
    value: function off(event) {
      if (this.events[event]) {
        this.events[event] = [];
      }
    }

    /**
       * Trigger event with params
       *
       * @param {string} event - Event to trigger
       * @param {object} params - Parameters to pass to event handler
       * @return {void}
       */

  }, {
    key: "trigger",
    value: function trigger(event, params) {
      if (this.events[event] && this.events[event].length) {
        this.events[event].forEach(function (handler) {
          return handler(params);
        });
      }
    }
  }]);

  return Events;
}();

exports.default = Events;

/***/ }),
/* 5 */
/***/ (function(module, exports) {

// removed by extract-text-webpack-plugin

/***/ })
/******/ ]);
});
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly8vd2VicGFjay91bml2ZXJzYWxNb2R1bGVEZWZpbml0aW9uIiwid2VicGFjazovLy93ZWJwYWNrL2Jvb3RzdHJhcCBiMTVlZjhiODY1NDdlZmVlNTk1NyIsIndlYnBhY2s6Ly8vLi9zcmMvanMvaW5kZXguanMiLCJ3ZWJwYWNrOi8vLy4vc3JjL2pzL3RpbWVwaWNrZXIuanMiLCJ3ZWJwYWNrOi8vLy4vc3JjL2pzL3RlbXBsYXRlLmpzIiwid2VicGFjazovLy8uL3NyYy9qcy9hc3NpZ24uanMiLCJ3ZWJwYWNrOi8vLy4vc3JjL2pzL2V2ZW50cy5qcyIsIndlYnBhY2s6Ly8vLi9zcmMvc2Fzcy9tYWluLnNjc3MiXSwibmFtZXMiOlsiVGltZVBpY2tlciIsInRlbXBsYXRlIiwiZGVmYXVsdE9wdGlvbnMiLCJ0aW1lRm9ybWF0IiwiYXV0b05leHQiLCJjYWNoZWRFbHMiLCJldmVudHMiLCJzZXR1cFRlbXBsYXRlIiwiYm9keSIsImRvY3VtZW50IiwiZ2V0RWxlbWVudHNCeUNsYXNzTmFtZSIsIm92ZXJsYXkiLCJ3cmFwcGVyIiwicGlja2VyIiwibWVyaWRpZW0iLCJtZXJpZGllbVNwYW5zIiwiZ2V0RWxlbWVudHNCeVRhZ05hbWUiLCJkaXNwbGF5SG91cnMiLCJkaXNwbGF5TWludXRlcyIsImRpc3BsYXlNZXJpZGllbSIsImJ1dHRvbkNhbmNlbCIsImJ1dHRvbkJhY2siLCJidXR0b25OZXh0IiwiYnV0dG9uRmluaXNoIiwiY2xvY2tIb3VycyIsImNsb2NrTWludXRlcyIsImNsb2NrTWlsaXRhcnlIb3VycyIsImNsb2NrSGFuZCIsImNsb2NrSG91cnNMaSIsImNsb2NrTWludXRlc0xpIiwiY2xvY2tNaWxpdGFyeUhvdXJzTGkiLCJzZXRFdmVudHMiLCJpbnB1dEVsIiwib3B0aW9ucyIsImVsZW1lbnQiLCJIVE1MRWxlbWVudCIsInF1ZXJ5U2VsZWN0b3IiLCJtdHBPcHRpb25zIiwiYWRkRXZlbnRMaXN0ZW5lciIsInNob3dFdmVudCIsImV2ZW50Iiwic2hvdyIsImlzVGVtcGxhdGVJbkRPTSIsImluc2VydEFkamFjZW50SFRNTCIsImhhc1NldEV2ZW50cyIsImhpZGVFdmVudCIsInNob3dNaW51dGVzIiwic2hvd0hvdXJzIiwiZmluaXNoIiwiZm9yRWFjaCIsImNhbGwiLCJzcGFuIiwibWVyaWRpZW1TZWxlY3RFdmVudCIsImhvdXIiLCJob3VyU2VsZWN0RXZlbnQiLCJtaW51dGUiLCJtaW51dGVTZWxlY3RFdmVudCIsImNsYXNzTGlzdCIsImFkZCIsImlzTWlsaXRhcnlGb3JtYXQiLCJibHVyIiwidG9nZ2xlSG91cnNWaXNpYmxlIiwidG9nZ2xlTWludXRlc1Zpc2libGUiLCJzZXREaXNwbGF5VGltZSIsImhvdXJzIiwibWludXRlcyIsInN0eWxlIiwib3ZlcmZsb3ciLCJkaXNwbGF5IiwiaGVpZ2h0IiwidHJpZ2dlciIsInRhcmdldCIsImRpc3BhdGNoRXZlbnQiLCJFdmVudCIsInJlc2V0U3RhdGUiLCJzdG9wUHJvcGFnYXRpb24iLCJhbGxvd2VkQ2xhc3NlcyIsImlzQWxsb3dlZCIsInNvbWUiLCJjb250YWlucyIsImFsbG93ZWRDbGFzcyIsImhpZGUiLCJjdXJyZW50U3RlcCIsIlN0cmluZyIsImlubmVySFRNTCIsInRyaW0iLCJtaW4iLCJudW1lcmljSG91ciIsInBhcnNlSW50IiwibnVtZXJpY01pbnV0ZSIsIm5vZGVJbmRleCIsImluY3JlbWVudCIsInJvdGF0ZURlZyIsInN0eWxlVmFsIiwidHJhbnNmb3JtIiwiaG91ckVscyIsInJvdGF0ZUhhbmQiLCJnZXRBY3RpdmVJbmRleCIsIm1pbnV0ZUVscyIsInRpbWVTZWxlY3RlZCIsImlzVmlzaWJsZSIsInRpbWVFbHMiLCJhY3RpdmVJbmRleCIsInRpbWVFbCIsImluZGV4IiwidGltZVZhbHVlIiwidmFsdWUiLCJjb250YWluZXJFbCIsImFjdGl2ZUVsIiwiYWN0aXZlQ2xhc3NOYW1lIiwiY3VycmVudEFjdGl2ZSIsInJlbW92ZSIsImlzRXF1YWxOb2RlIiwibGlzdEVscyIsIm5ld0FjdGl2ZSIsInBhcmVudEVsIiwicGFyZW50RWxlbWVudCIsImlzSW5uZXIiLCJzZXRBY3RpdmVFbCIsIkJvb2xlYW4iLCJhc3NpZ24iLCJUeXBlRXJyb3IiLCJ0byIsIk9iamVjdCIsImluYyIsIm5leHRTb3VyY2UiLCJrZXlzQXJyYXkiLCJrZXlzIiwibmV4dEluZGV4IiwibGVuIiwibGVuZ3RoIiwibmV4dEtleSIsImRlc2MiLCJnZXRPd25Qcm9wZXJ0eURlc2NyaXB0b3IiLCJlbnVtZXJhYmxlIiwiRXZlbnRzIiwiaGFuZGxlciIsInB1c2giLCJwYXJhbXMiXSwibWFwcGluZ3MiOiJBQUFBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLENBQUM7QUFDRCxPO0FDVkE7QUFDQTs7QUFFQTtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQUVBO0FBQ0E7O0FBRUE7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7OztBQUdBO0FBQ0E7O0FBRUE7QUFDQTs7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLGFBQUs7QUFDTDtBQUNBOztBQUVBO0FBQ0E7QUFDQTtBQUNBLG1DQUEyQiwwQkFBMEIsRUFBRTtBQUN2RCx5Q0FBaUMsZUFBZTtBQUNoRDtBQUNBO0FBQ0E7O0FBRUE7QUFDQSw4REFBc0QsK0RBQStEOztBQUVySDtBQUNBOztBQUVBO0FBQ0E7Ozs7Ozs7Ozs7Ozs7OztBQzdEQTs7Ozs7O1FBQ1NBLFU7Ozs7Ozs7Ozs7Ozs7Ozs7O0FDRFQ7Ozs7QUFDQTs7OztBQUNBOzs7O0FBQ0E7Ozs7OztBQUVBOzs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7OztJQTZCTUEsVTs7QUFRSjs7Ozs7QUFLQSx3QkFBYztBQUFBOztBQUFBLFNBWmRDLFFBWWM7QUFBQSxTQVhkQyxjQVdjLEdBWEc7QUFDZkMsa0JBQVksVUFERztBQUVmQyxnQkFBVTtBQUZLLEtBV0g7QUFBQSxTQVBkQyxTQU9jLEdBUEYsRUFPRTs7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QWI7O0FBRUEsVUFBSUMsU0FBUyxXQUFULElBQXdCQSxLQUFLRSxVQUFqQyxFQUE2QztBQUMzQ1osV0FBR1MsT0FBSCxJQUFjTixXQUFXTSxPQUFYLENBQWQ7QUFDRDtBQUNGO0FBQ0Y7O0FBRUQsU0FBT1QsRUFBUDtBQUNEOztrQkFFY0YsTTs7Ozs7Ozs7Ozs7Ozs7Ozs7QUMzQ2Y7Ozs7O0lBS3FCZSxNOzs7O1NBQ25CakksTSxHQUFTLEU7Ozs7Ozs7QUFFVDs7Ozs7Ozt1QkFPR2tDLEssRUFBT2dHLE8sRUFBUztBQUNqQixVQUFJLENBQUMsS0FBS2xJLE1BQUwsQ0FBWWtDLEtBQVosQ0FBTCxFQUF5QjtBQUN2QixhQUFLbEMsTUFBTCxDQUFZa0MsS0FBWixJQUFxQixFQUFyQjtBQUNEOztBQUVELFdBQUtsQyxNQUFMLENBQVlrQyxLQUFaLEVBQW1CaUcsSUFBbkIsQ0FBd0JELE9BQXhCO0FBQ0Q7O0FBRUQ7Ozs7Ozs7Ozt3QkFNSWhHLEssRUFBTztBQUNULFVBQUksS0FBS2xDLE1BQUwsQ0FBWWtDLEtBQVosQ0FBSixFQUF3QjtBQUN0QixhQUFLbEMsTUFBTCxDQUFZa0MsS0FBWixJQUFxQixFQUFyQjtBQUNEO0FBQ0Y7O0FBRUQ7Ozs7Ozs7Ozs7NEJBT1FBLEssRUFBT2tHLE0sRUFBUTtBQUNyQixVQUFJLEtBQUtwSSxNQUFMLENBQVlrQyxLQUFaLEtBQXNCLEtBQUtsQyxNQUFMLENBQVlrQyxLQUFaLEVBQW1CMEYsTUFBN0MsRUFBcUQ7QUFDbkQsYUFBSzVILE1BQUwsQ0FBWWtDLEtBQVosRUFBbUJTLE9BQW5CLENBQTJCO0FBQUEsaUJBQVd1RixRQUFRRSxNQUFSLENBQVg7QUFBQSxTQUEzQjtBQUNEO0FBQ0Y7Ozs7OztrQkF6Q2tCSCxNOzs7Ozs7QUNMckIseUMiLCJmaWxlIjoiVGltZVBpY2tlci5qcyIsInNvdXJjZXNDb250ZW50IjpbIihmdW5jdGlvbiB3ZWJwYWNrVW5pdmVyc2FsTW9kdWxlRGVmaW5pdGlvbihyb290LCBmYWN0b3J5KSB7XG5cdGlmKHR5cGVvZiBleHBvcnRzID09PSAnb2JqZWN0JyAmJiB0eXBlb2YgbW9kdWxlID09PSAnb2JqZWN0Jylcblx0XHRtb2R1bGUuZXhwb3J0cyA9IGZhY3RvcnkoKTtcblx0ZWxzZSBpZih0eXBlb2YgZGVmaW5lID09PSAnZnVuY3Rpb24nICYmIGRlZmluZS5hbWQpXG5cdFx0ZGVmaW5lKFtdLCBmYWN0b3J5KTtcblx0ZWxzZSBpZih0eXBlb2YgZXhwb3J0cyA9PT0gJ29iamVjdCcpXG5cdFx0ZXhwb3J0c1tcIlRpbWVQaWNrZXJcIl0gPSBmYWN0b3J5KCk7XG5cdGVsc2Vcblx0XHRyb290W1wiVGltZVBpY2tlclwiXSA9IGZhY3RvcnkoKTtcbn0pKHRoaXMsIGZ1bmN0aW9uKCkge1xucmV0dXJuIFxuXG5cbi8vIFdFQlBBQ0sgRk9PVEVSIC8vXG4vLyB3ZWJwYWNrL3VuaXZlcnNhbE1vZHVsZURlZmluaXRpb24iLCIgXHQvLyBUaGUgbW9kdWxlIGNhY2hlXG4gXHR2YXIgaW5zdGFsbGVkTW9kdWxlcyA9IHt9O1xuXG4gXHQvLyBUaGUgcmVxdWlyZSBmdW5jdGlvblxuIFx0ZnVuY3Rpb24gX193ZWJwYWNrX3JlcXVpcmVfXyhtb2R1bGVJZCkge1xuXG4gXHRcdC8vIENoZWNrIGlmIG1vZHVsZSBpcyBpbiBjYWNoZVxuIFx0XHRpZihpbnN0YWxsZWRNb2R1bGVzW21vZHVsZUlkXSkge1xuIFx0XHRcdHJldHVybiBpbnN0YWxsZWRNb2R1bGVzW21vZHVsZUlkXS5leHBvcnRzO1xuIFx0XHR9XG4gXHRcdC8vIENyZWF0ZSBhIG5ldyBtb2R1bGUgKGFuZCBwdXQgaXQgaW50byB0aGUgY2FjaGUpXG4gXHRcdHZhciBtb2R1bGUgPSBpbnN0YWxsZWRNb2R1bGVzW21vZHVsZUlkXSA9IHtcbiBcdFx0XHRpOiBtb2R1bGVJZCxcbiBcdFx0XHRsOiBmYWxzZSxcbiBcdFx0XHRleHBvcnRzOiB7fVxuIFx0XHR9O1xuXG4gXHRcdC8vIEV4ZWN1dGUgdGhlIG1vZHVsZSBmdW5jdGlvblxuIFx0XHRtb2R1bGVzW21vZHVsZUlkXS5jYWxsKG1vZHVsZS5leHBvcnRzLCBtb2R1bGUsIG1vZHVsZS5leHBvcnRzLCBfX3dlYnBhY2tfcmVxdWlyZV9fKTtcblxuIFx0XHQvLyBGbGFnIHRoZSBtb2R1bGUgYXMgbG9hZGVkXG4gXHRcdG1vZHVsZS5sID0gdHJ1ZTtcblxuIFx0XHQvLyBSZXR1cm4gdGhlIGV4cG9ydHMgb2YgdGhlIG1vZHVsZVxuIFx0XHRyZXR1cm4gbW9kdWxlLmV4cG9ydHM7XG4gXHR9XG5cblxuIFx0Ly8gZXhwb3NlIHRoZSBtb2R1bGVzIG9iamVjdCAoX193ZWJwYWNrX21vZHVsZXNfXylcbiBcdF9fd2VicGFja19yZXF1aXJlX18ubSA9IG1vZHVsZXM7XG5cbiBcdC8vIGV4cG9zZSB0aGUgbW9kdWxlIGNhY2hlXG4gXHRfX3dlYnBhY2tfcmVxdWlyZV9fLmMgPSBpbnN0YWxsZWRNb2R1bGVzO1xuXG4gXHQvLyBkZWZpbmUgZ2V0dGVyIGZ1bmN0aW9uIGZvciBoYXJtb255IGV4cG9ydHNcbiBcdF9fd2VicGFja19yZXF1aXJlX18uZCA9IGZ1bmN0aW9uKGV4cG9ydHMsIG5hbWUsIGdldHRlcikge1xuIFx0XHRpZighX193ZWJwYWNrX3JlcXVpcmVfXy5vKGV4cG9ydHMsIG5hbWUpKSB7XG4gXHRcdFx0T2JqZWN0LmRlZmluZVByb3BlcnR5KGV4cG9ydHMsIG5hbWUsIHtcbiBcdFx0XHRcdGNvbmZpZ3VyYWJsZTogZmFsc2UsXG4gXHRcdFx0XHRlbnVtZXJhYmxlOiB0cnVlLFxuIFx0XHRcdFx0Z2V0OiBnZXR0ZXJcbiBcdFx0XHR9KTtcbiBcdFx0fVxuIFx0fTtcblxuIFx0Ly8gZ2V0RGVmYXVsdEV4cG9ydCBmdW5jdGlvbiBmb3IgY29tcGF0aWJpbGl0eSB3aXRoIG5vbi1oYXJtb255IG1vZHVsZXNcbiBcdF9fd2VicGFja19yZXF1aXJlX18ubiA9IGZ1bmN0aW9uKG1vZHVsZSkge1xuIFx0XHR2YXIgZ2V0dGVyID0gbW9kdWxlICYmIG1vZHVsZS5fX2VzTW9kdWxlID9cbiBcdFx0XHRmdW5jdGlvbiBnZXREZWZhdWx0KCkgeyByZXR1cm4gbW9kdWxlWydkZWZhdWx0J107IH0gOlxuIFx0XHRcdGZ1bmN0aW9uIGdldE1vZHVsZUV4cG9ydHMoKSB7IHJldHVybiBtb2R1bGU7IH07XG4gXHRcdF9fd2VicGFja19yZXF1aXJlX18uZChnZXR0ZXIsICdhJywgZ2V0dGVyKTtcbiBcdFx0cmV0dXJuIGdldHRlcjtcbiBcdH07XG5cbiBcdC8vIE9iamVjdC5wcm90b3R5cGUuaGFzT3duUHJvcGVydHkuY2FsbFxuIFx0X193ZWJwYWNrX3JlcXVpcmVfXy5vID0gZnVuY3Rpb24ob2JqZWN0LCBwcm9wZXJ0eSkgeyByZXR1cm4gT2JqZWN0LnByb3RvdHlwZS5oYXNPd25Qcm9wZXJ0eS5jYWxsKG9iamVjdCwgcHJvcGVydHkpOyB9O1xuXG4gXHQvLyBfX3dlYnBhY2tfcHVibGljX3BhdGhfX1xuIFx0X193ZWJwYWNrX3JlcXVpcmVfXy5wID0gXCJcIjtcblxuIFx0Ly8gTG9hZCBlbnRyeSBtb2R1bGUgYW5kIHJldHVybiBleHBvcnRzXG4gXHRyZXR1cm4gX193ZWJwYWNrX3JlcXVpcmVfXyhfX3dlYnBhY2tfcmVxdWlyZV9fLnMgPSAwKTtcblxuXG5cbi8vIFdFQlBBQ0sgRk9PVEVSIC8vXG4vLyB3ZWJwYWNrL2Jvb3RzdHJhcCBiMTVlZjhiODY1NDdlZmVlNTk1NyIsImltcG9ydCBUaW1lUGlja2VyIGZyb20gJy4vdGltZXBpY2tlcidcbmV4cG9ydCB7IFRpbWVQaWNrZXIgfTtcblxuXG5cbi8vIFdFQlBBQ0sgRk9PVEVSIC8vXG4vLyAuL3NyYy9qcy9pbmRleC5qcyIsImltcG9ydCB0ZW1wbGF0ZSBmcm9tICcuL3RlbXBsYXRlJ1xuaW1wb3J0IGFzc2lnbiBmcm9tICcuL2Fzc2lnbidcbmltcG9ydCBFdmVudHMgZnJvbSAnLi9ldmVudHMnXG5pbXBvcnQgJy4uL3Nhc3MvbWFpbi5zY3NzJ1xuXG4vKipcbiAqIEBjbGFzcyBUaW1lUGlja2VyXG4gKlxuICogQHByb3Age3N0cmluZ30gdGVtcGxhdGUgLSBUaW1lUGlja2VyIHRlbXBsYXRlXG4gKiBAcHJvcCB7b2JqZWN0fSBkZWZhdWx0T3B0aW9ucyAtIERlZmF1bHQgY29uZmlnIG9wdGlvbnNcbiAqIEBwcm9wIHtzdHJpbmd9IGRlZmF1bHRPcHRpb25zLnRpbWVGb3JtYXQgLSAxMiBvciAyNCBob3VyIGZvcm1hdCBbJ3N0YW5kYXJkJywgJ21pbGl0YXJ5J11cbiAqIEBwcm9wIHtib29sfSBkZWZhdWx0T3B0aW9ucy5hdXRvTmV4dCAtIEF1dG8tbmV4dCBvbiB0aW1lIGVsZW1lbnQgc2VsZWN0XG4gKiBAcHJvcCB7b2JqZWN0fSBjYWNoZWRFbHMgLSBDYWNoZWQgZWxlbWVudHMgaW4gdGVtcGxhdGVcbiAqIEBwcm9wIHtIVE1MRWxlbWVudH0gY2FjaGVkRWxzLmJvZHkgLSBkb2N1bWVudC5ib2R5XG4gKiBAcHJvcCB7SFRNTEVsZW1lbnR9IGNhY2hlZEVscy5vdmVybGF5IC0gT3ZlcmxheSBlbGVtZW50ICgnLm10cC1vdmVybGF5JylbMF1cbiAqIEBwcm9wIHtIVE1MRWxlbWVudH0gY2FjaGVkRWxzLndyYXBwZXIgLSBXcmFwcGVyIGVsZW1lbnQgKCcubXRwLXdyYXBwZXInKVswXVxuICogQHByb3Age0hUTUxFbGVtZW50fSBjYWNoZWRFbHMucGlja2VyIC0gU2VsZWN0aW9uIGVsZW1lbnRzIHdyYXBwZXIgKCcubXRwLXBpY2tlcicpWzBdXG4gKiBAcHJvcCB7SFRNTEVsZW1lbnR9IGNhY2hlZEVscy5tZXJpZGllbSAtIE1lcmlkaWVtIHNlbGVjdGlvbiBlbGVtZW50cyB3cmFwcGVyICgnLm10cC1tZXJpZGllbScpWzBdXG4gKiBAcHJvcCB7SFRNTENvbGxlY3Rpb259IGNhY2hlZEVscy5tZXJpZGllbVNwYW5zIC0gTWVyaWRpZW0gc2VsZWN0aW9uIGVsZW1lbnRzIG1lcmlkaWVtKCdzcGFuJylcbiAqIEBwcm9wIHtIVE1MRWxlbWVudH0gY2FjaGVkRWxzLmRpc3BsYXlIb3VycyAtIFNlbGVjdGVkIGhvdXIgZGlzcGxheSBlbGVtZW50ICgnLm10cC1kaXNwbGF5X19ob3VycycpWzBdXG4gKiBAcHJvcCB7SFRNTEVsZW1lbnR9IGNhY2hlZEVscy5kaXNwbGF5TWludXRlcyAtIFNlbGVjdGVkIG1pbnV0ZXMgZGlzcGxheSBlbGVtZW50ICgnLm10cC1kaXNwbGF5X19taW51dGVzJylbMF1cbiAqIEBwcm9wIHtIVE1MRWxlbWVudH0gY2FjaGVkRWxzLmRpc3BsYXlNZXJkaWVtIC0gU2VsZWN0ZWQgbWVyaWRpZW0gZGlzcGxheSBlbGVtZW50ICgnLm10cC1kaXNwbGF5X19tZXJpZGllbScpWzBdXG4gKiBAcHJvcCB7SFRNTEVsZW1lbnR9IGNhY2hlZEVscy5idXR0b25DYW5jZWwgLSBDYW5jZWwgYnV0dG9uIGVsZW1lbnQgKCcubXRwLWFjdGlvbnNfX2NhbmNlbCcpWzBdXG4gKiBAcHJvcCB7SFRNTEVsZW1lbnR9IGNhY2hlZEVscy5idXR0b25CYWNrIC0gQmFjayBidXR0b24gZWxlbWVudCAoJy5tdHAtYWN0aW9uc19fYmFjaycpWzBdXG4gKiBAcHJvcCB7SFRNTEVsZW1lbnR9IGNhY2hlZEVscy5idXR0b25OZXh0IC0gTmV4dCBidXR0b24gZWxlbWVudCAoJy5tdHAtYWN0aW9uc19fbmV4dCcpWzBdXG4gKiBAcHJvcCB7SFRNTEVsZW1lbnR9IGNhY2hlZEVscy5idXR0b25GaW5pc2ggLSBGaW5pc2ggYnV0dG9uIGVsZW1lbnQgKCcubXRwLWFjdGlvbnNfX2ZpbmlzaCcpWzBdXG4gKiBAcHJvcCB7SFRNTEVsZW1lbnR9IGNhY2hlZEVscy5jbG9ja0hvdXJzIC0gSG91ciBlbGVtZW50cyBkaXNwbGF5IHdyYXBwZXIgKCcubXRwLWNsb2NrX19ob3VycycpWzBdXG4gKiBAcHJvcCB7SFRNTEVsZW1lbnR9IGNhY2hlZEVscy5jbG9ja01pbnV0ZXMgLSBNaW51dGUgZWxlbWVudHMgZGlzcGxheSB3cmFwcGVyICgnLm10cC1jbG9ja19fbWludXRlcycpWzBdXG4gKiBAcHJvcCB7SFRNTEVsZW1lbnR9IGNhY2hlZEVscy5jbG9ja01pbGl0YXJ5SG91cnMgLSBNaWxpdGFyeSBob3VyIGVsZW1lbnRzIGRpc3BsYXkgd3JhcHBlciAoJy5tdHBfY2xvY2tfX2hvdXJzLS1taWxpdGFyeScpWzBdXG4gKiBAcHJvcCB7SFRNTEVsZW1lbnR9IGNhY2hlZEVscy5jbG9ja0hhbmQgLSBDbG9jayBoYW5kIGRpc3BsYXkgKCcubXRwLWNsb2NrX19oYW5kJylbMF1cbiAqIEBwcm9wIHtIVE1MQ29sbGVjdGlvbn0gY2FjaGVkRWxzLmNsb2NrSG91cnNMaSAtIEhvdXIgbGlzdCBlbGVtZW50cyBjbG9ja0hvdXJzKCdsaScpXG4gKiBAcHJvcCB7SFRNTENvbGxlY3Rpb259IGNhY2hlZEVscy5jbG9ja01pbnV0ZXNMaSAtIE1pbnV0ZSBsaXN0IGVsZW1lbnRzIGNsb2NrTWludXRlcygnbGknKVxuICogQHByb3Age0hUTUxDb2xsZWN0aW9ufSBjYWNoZWRFbHMuY2xvY2tNaWxpdGFyeUhvdXJzTGkgLSBNaWxpdGFyeSBIb3VyIGxpIGVsZW1lbnRzIGNsb2NrTWlsaXRhcnlIb3VycygnbGknKVxuICovXG5jbGFzcyBUaW1lUGlja2VyIHtcbiAgdGVtcGxhdGUgPSB0ZW1wbGF0ZVxuICBkZWZhdWx0T3B0aW9ucyA9IHtcbiAgICB0aW1lRm9ybWF0OiAnc3RhbmRhcmQnLFxuICAgIGF1dG9OZXh0OiBmYWxzZSxcbiAgfVxuICBjYWNoZWRFbHMgPSB7fVxuXG4gIC8qKlxuICAgICAqIEluaXRpYWxpemUgbmV3IFRpbWVQaWNrZXIgaW5zdGFuY2VcbiAgICAgKlxuICAgICAqIEByZXR1cm4ge1RpbWVQaWNrZXJ9IE5ldyBUaW1lUGlja2VyIGluc3RhbmNlXG4gICAgICovXG4gIGNvbnN0cnVjdG9yKCkge1xuICAgIHRoaXMuZXZlbnRzID0gbmV3IEV2ZW50cygpXG5cbiAgICB0aGlzLnNldHVwVGVtcGxhdGUoKVxuXG4gICAgdGhpcy5jYWNoZWRFbHMuYm9keSA9IGRvY3VtZW50LmJvZHlcbiAgICA7W3RoaXMuY2FjaGVkRWxzLm92ZXJsYXldID0gdGhpcy5jYWNoZWRFbHMuYm9keS5nZXRFbGVtZW50c0J5Q2xhc3NOYW1lKFxuICAgICAgJ210cC1vdmVybGF5JyxcbiAgICApXG4gICAgO1t0aGlzLmNhY2hlZEVscy53cmFwcGVyXSA9IHRoaXMuY2FjaGVkRWxzLm92ZXJsYXkuZ2V0RWxlbWVudHNCeUNsYXNzTmFtZShcbiAgICAgICdtdHAtd3JhcHBlcicsXG4gICAgKVxuICAgIDtbdGhpcy5jYWNoZWRFbHMucGlja2VyXSA9IHRoaXMuY2FjaGVkRWxzLndyYXBwZXIuZ2V0RWxlbWVudHNCeUNsYXNzTmFtZShcbiAgICAgICdtdHAtcGlja2VyJyxcbiAgICApXG4gICAgO1t0aGlzLmNhY2hlZEVscy5tZXJpZGllbV0gPSB0aGlzLmNhY2hlZEVscy53cmFwcGVyLmdldEVsZW1lbnRzQnlDbGFzc05hbWUoXG4gICAgICAnbXRwLW1lcmlkaWVtJyxcbiAgICApXG4gICAgdGhpcy5jYWNoZWRFbHMubWVyaWRpZW1TcGFucyA9IHRoaXMuY2FjaGVkRWxzLm1lcmlkaWVtLmdldEVsZW1lbnRzQnlUYWdOYW1lKFxuICAgICAgJ3NwYW4nLFxuICAgIClcbiAgICA7W1xuICAgICAgdGhpcy5jYWNoZWRFbHMuZGlzcGxheUhvdXJzLFxuICAgIF0gPSB0aGlzLmNhY2hlZEVscy53cmFwcGVyLmdldEVsZW1lbnRzQnlDbGFzc05hbWUoJ210cC1kaXNwbGF5X19ob3VycycpXG4gICAgO1tcbiAgICAgIHRoaXMuY2FjaGVkRWxzLmRpc3BsYXlNaW51dGVzLFxuICAgIF0gPSB0aGlzLmNhY2hlZEVscy53cmFwcGVyLmdldEVsZW1lbnRzQnlDbGFzc05hbWUoJ210cC1kaXNwbGF5X19taW51dGVzJylcbiAgICA7W1xuICAgICAgdGhpcy5jYWNoZWRFbHMuZGlzcGxheU1lcmlkaWVtLFxuICAgIF0gPSB0aGlzLmNhY2hlZEVscy53cmFwcGVyLmdldEVsZW1lbnRzQnlDbGFzc05hbWUoJ210cC1kaXNwbGF5X19tZXJpZGllbScpXG4gICAgO1tcbiAgICAgIHRoaXMuY2FjaGVkRWxzLmJ1dHRvbkNhbmNlbCxcbiAgICBdID0gdGhpcy5jYWNoZWRFbHMucGlja2VyLmdldEVsZW1lbnRzQnlDbGFzc05hbWUoJ210cC1hY3Rpb25zX19jYW5jZWwnKVxuICAgIDtbdGhpcy5jYWNoZWRFbHMuYnV0dG9uQmFja10gPSB0aGlzLmNhY2hlZEVscy5waWNrZXIuZ2V0RWxlbWVudHNCeUNsYXNzTmFtZShcbiAgICAgICdtdHAtYWN0aW9uc19fYmFjaycsXG4gICAgKVxuICAgIDtbdGhpcy5jYWNoZWRFbHMuYnV0dG9uTmV4dF0gPSB0aGlzLmNhY2hlZEVscy5waWNrZXIuZ2V0RWxlbWVudHNCeUNsYXNzTmFtZShcbiAgICAgICdtdHAtYWN0aW9uc19fbmV4dCcsXG4gICAgKVxuICAgIDtbXG4gICAgICB0aGlzLmNhY2hlZEVscy5idXR0b25GaW5pc2gsXG4gICAgXSA9IHRoaXMuY2FjaGVkRWxzLnBpY2tlci5nZXRFbGVtZW50c0J5Q2xhc3NOYW1lKCdtdHAtYWN0aW9uc19fZmluaXNoJylcbiAgICA7W3RoaXMuY2FjaGVkRWxzLmNsb2NrSG91cnNdID0gdGhpcy5jYWNoZWRFbHMucGlja2VyLmdldEVsZW1lbnRzQnlDbGFzc05hbWUoXG4gICAgICAnbXRwLWNsb2NrX19ob3VycycsXG4gICAgKVxuICAgIDtbXG4gICAgICB0aGlzLmNhY2hlZEVscy5jbG9ja01pbnV0ZXMsXG4gICAgXSA9IHRoaXMuY2FjaGVkRWxzLnBpY2tlci5nZXRFbGVtZW50c0J5Q2xhc3NOYW1lKCdtdHAtY2xvY2tfX21pbnV0ZXMnKVxuICAgIDtbXG4gICAgICB0aGlzLmNhY2hlZEVscy5jbG9ja01pbGl0YXJ5SG91cnMsXG4gICAgXSA9IHRoaXMuY2FjaGVkRWxzLnBpY2tlci5nZXRFbGVtZW50c0J5Q2xhc3NOYW1lKFxuICAgICAgJ210cC1jbG9ja19faG91cnMtbWlsaXRhcnknLFxuICAgIClcbiAgICA7W3RoaXMuY2FjaGVkRWxzLmNsb2NrSGFuZF0gPSB0aGlzLmNhY2hlZEVscy5waWNrZXIuZ2V0RWxlbWVudHNCeUNsYXNzTmFtZShcbiAgICAgICdtdHAtY2xvY2tfX2hhbmQnLFxuICAgIClcbiAgICB0aGlzLmNhY2hlZEVscy5jbG9ja0hvdXJzTGkgPSB0aGlzLmNhY2hlZEVscy5jbG9ja0hvdXJzLmdldEVsZW1lbnRzQnlUYWdOYW1lKFxuICAgICAgJ2xpJyxcbiAgICApXG4gICAgdGhpcy5jYWNoZWRFbHMuY2xvY2tNaW51dGVzTGkgPSB0aGlzLmNhY2hlZEVscy5jbG9ja01pbnV0ZXMuZ2V0RWxlbWVudHNCeVRhZ05hbWUoXG4gICAgICAnbGknLFxuICAgIClcbiAgICB0aGlzLmNhY2hlZEVscy5jbG9ja01pbGl0YXJ5SG91cnNMaSA9IHRoaXMuY2FjaGVkRWxzLmNsb2NrTWlsaXRhcnlIb3Vycy5nZXRFbGVtZW50c0J5VGFnTmFtZShcbiAgICAgICdsaScsXG4gICAgKVxuXG4gICAgdGhpcy5zZXRFdmVudHMoKVxuICB9XG5cbiAgLyoqXG4gICAgICogQmluZCBldmVudCB0byB0aGUgaW5wdXQgZWxlbWVudCB0byBvcGVuIHdoZW4gYGZvY3VzYCBldmVudCBpcyBldmVudHMudHJpZ2dlcmVkXG4gICAgICpcbiAgICAgKiBAcGFyYW0ge3N0cmluZ3xIVE1MRWxlbWVudH0gaW5wdXRFbCBTZWxlY3RvciBlbGVtZW50IHRvIGJlIHF1ZXJpZWQgb3IgZXhpc3RpbmcgSFRNTEVsZW1lbnRcbiAgICAgKiBAcGFyYW0ge29iamVjdH0gb3B0aW9ucyBPcHRpb25zIHRvIG1lcmdlZCB3aXRoIGRlZmF1bHRzIGFuZCBzZXQgdG8gaW5wdXQgZWxlbWVudCBvYmplY3RcbiAgICAgKiBAcmV0dXJuIHt2b2lkfVxuICAgICAqL1xuICBiaW5kSW5wdXQoaW5wdXRFbCwgb3B0aW9ucyA9IHt9KSB7XG4gICAgY29uc3QgZWxlbWVudCA9XG4gICAgICBpbnB1dEVsIGluc3RhbmNlb2YgSFRNTEVsZW1lbnQgPyBpbnB1dEVsIDogZG9jdW1lbnQucXVlcnlTZWxlY3RvcihpbnB1dEVsKVxuXG4gICAgZWxlbWVudC5tdHBPcHRpb25zID0gYXNzaWduKHt9LCB0aGlzLmRlZmF1bHRPcHRpb25zLCBvcHRpb25zKVxuICAgIGVsZW1lbnQuYWRkRXZlbnRMaXN0ZW5lcignZm9jdXMnLCBldmVudCA9PiB0aGlzLnNob3dFdmVudChldmVudCkpXG4gIH1cblxuICAvKipcbiAgICAgKiBPcGVuIHBpY2tlciB3aXRoIHRoZSBpbnB1dCBwcm92aWRlZCBpbiBjb250ZXh0IHdpdGhvdXQgYmluZGluZyBldmVudHNcbiAgICAgKlxuICAgICAqIEBwYXJhbSB7c3RyaW5nfEhUTUxFbGVtZW50fSBpbnB1dEVsIFNlbGVjdG9yIGVsZW1lbnQgdG8gYmUgcXVlcmllZCBvciBleGlzdGluZyBIVE1MRWxlbWVudFxuICAgICAqIEBwYXJhbSB7b2JqZWN0fSBvcHRpb25zIE9wdGlvbnMgdG8gbWVyZ2VkIHdpdGggZGVmYXVsdHMgYW5kIHNldCB0byBpbnB1dCBlbGVtZW50IG9iamVjdFxuICAgICAqIEByZXR1cm4ge3ZvaWR9XG4gICAgICovXG4gIG9wZW5PbklucHV0KGlucHV0RWwsIG9wdGlvbnMgPSB7fSkge1xuICAgIHRoaXMuaW5wdXRFbCA9XG4gICAgICBpbnB1dEVsIGluc3RhbmNlb2YgSFRNTEVsZW1lbnQgPyBpbnB1dEVsIDogZG9jdW1lbnQucXVlcnlTZWxlY3RvcihpbnB1dEVsKVxuICAgIHRoaXMuaW5wdXRFbC5tdHBPcHRpb25zID0gYXNzaWduKHt9LCB0aGlzLmRlZmF1bHRPcHRpb25zLCBvcHRpb25zKVxuICAgIHRoaXMuc2hvdygpXG4gIH1cblxuICAvKipcbiAgICAgKiBTZXR1cCB0aGUgdGVtcGxhdGUgaW4gRE9NIGlmIG5vdCBhbHJlYWR5XG4gICAgICpcbiAgICAgKiBAcmV0dXJuIHt2b2lkfVxuICAgICAqL1xuICBzZXR1cFRlbXBsYXRlKCkge1xuICAgIGlmICghdGhpcy5pc1RlbXBsYXRlSW5ET00oKSkge1xuICAgICAgZG9jdW1lbnQuYm9keS5pbnNlcnRBZGphY2VudEhUTUwoJ2JlZm9yZWVuZCcsIHRlbXBsYXRlKVxuICAgIH1cbiAgfVxuXG4gIC8qKlxuICAgICAqIFNldCB0aGUgZXZlbnRzIG9uIHBpY2tlciBlbGVtZW50c1xuICAgICAqXG4gICAgICogQHJldHVybiB7dm9pZH1cbiAgICAgKi9cbiAgc2V0RXZlbnRzKCkge1xuICAgIGlmICghdGhpcy5oYXNTZXRFdmVudHMoKSkge1xuICAgICAgLy8gY2xvc2VcbiAgICAgIHRoaXMuY2FjaGVkRWxzLm92ZXJsYXkuYWRkRXZlbnRMaXN0ZW5lcignY2xpY2snLCBldmVudCA9PlxuICAgICAgICB0aGlzLmhpZGVFdmVudChldmVudCksXG4gICAgICApXG5cbiAgICAgIHRoaXMuY2FjaGVkRWxzLmJ1dHRvbkNhbmNlbC5hZGRFdmVudExpc3RlbmVyKCdjbGljaycsIGV2ZW50ID0+XG4gICAgICAgIHRoaXMuaGlkZUV2ZW50KGV2ZW50KSxcbiAgICAgIClcbiAgICAgIHRoaXMuY2FjaGVkRWxzLmJ1dHRvbk5leHQuYWRkRXZlbnRMaXN0ZW5lcignY2xpY2snLCAoKSA9PlxuICAgICAgICB0aGlzLnNob3dNaW51dGVzKCksXG4gICAgICApXG4gICAgICB0aGlzLmNhY2hlZEVscy5idXR0b25CYWNrLmFkZEV2ZW50TGlzdGVuZXIoJ2NsaWNrJywgKCkgPT5cbiAgICAgICAgdGhpcy5zaG93SG91cnMoKSxcbiAgICAgIClcbiAgICAgIHRoaXMuY2FjaGVkRWxzLmJ1dHRvbkZpbmlzaC5hZGRFdmVudExpc3RlbmVyKCdjbGljaycsICgpID0+IHRoaXMuZmluaXNoKCkpXG5cbiAgICAgIC8vIG1lcmlkaWVtIHNlbGVjdCBldmVudHNcbiAgICAgIDtbXS5mb3JFYWNoLmNhbGwodGhpcy5jYWNoZWRFbHMubWVyaWRpZW1TcGFucywgc3BhbiA9PiB7XG4gICAgICAgIHNwYW4uYWRkRXZlbnRMaXN0ZW5lcignY2xpY2snLCBldmVudCA9PiB0aGlzLm1lcmlkaWVtU2VsZWN0RXZlbnQoZXZlbnQpKVxuICAgICAgfSlcblxuICAgICAgLy8gdGltZSBzZWxlY3QgZXZlbnRzXG4gICAgICA7W10uZm9yRWFjaC5jYWxsKHRoaXMuY2FjaGVkRWxzLmNsb2NrSG91cnNMaSwgaG91ciA9PiB7XG4gICAgICAgIGhvdXIuYWRkRXZlbnRMaXN0ZW5lcignY2xpY2snLCBldmVudCA9PiB7XG4gICAgICAgICAgdGhpcy5ob3VyU2VsZWN0RXZlbnQoXG4gICAgICAgICAgICBldmVudCxcbiAgICAgICAgICAgIHRoaXMuY2FjaGVkRWxzLmNsb2NrSG91cnMsXG4gICAgICAgICAgICB0aGlzLmNhY2hlZEVscy5jbG9ja0hvdXJzTGksXG4gICAgICAgICAgKVxuICAgICAgICB9KVxuICAgICAgfSlcbiAgICAgIDtbXS5mb3JFYWNoLmNhbGwodGhpcy5jYWNoZWRFbHMuY2xvY2tNaWxpdGFyeUhvdXJzTGksIGhvdXIgPT4ge1xuICAgICAgICBob3VyLmFkZEV2ZW50TGlzdGVuZXIoJ2NsaWNrJywgZXZlbnQgPT4ge1xuICAgICAgICAgIHRoaXMuaG91clNlbGVjdEV2ZW50KFxuICAgICAgICAgICAgZXZlbnQsXG4gICAgICAgICAgICB0aGlzLmNhY2hlZEVscy5jbG9ja01pbGl0YXJ5SG91cnMsXG4gICAgICAgICAgICB0aGlzLmNhY2hlZEVscy5jbG9ja01pbGl0YXJ5SG91cnNMaSxcbiAgICAgICAgICApXG4gICAgICAgIH0pXG4gICAgICB9KVxuICAgICAgO1tdLmZvckVhY2guY2FsbCh0aGlzLmNhY2hlZEVscy5jbG9ja01pbnV0ZXNMaSwgbWludXRlID0+IHtcbiAgICAgICAgbWludXRlLmFkZEV2ZW50TGlzdGVuZXIoJ2NsaWNrJywgZXZlbnQgPT4ge1xuICAgICAgICAgIHRoaXMubWludXRlU2VsZWN0RXZlbnQoXG4gICAgICAgICAgICBldmVudCxcbiAgICAgICAgICAgIHRoaXMuY2FjaGVkRWxzLmNsb2NrTWludXRlcyxcbiAgICAgICAgICAgIHRoaXMuY2FjaGVkRWxzLmNsb2NrTWludXRlc0xpLFxuICAgICAgICAgIClcbiAgICAgICAgfSlcbiAgICAgIH0pXG5cbiAgICAgIHRoaXMuY2FjaGVkRWxzLndyYXBwZXIuY2xhc3NMaXN0LmFkZCgnbXRwLWV2ZW50cy1zZXQnKVxuICAgIH1cbiAgfVxuXG4gIC8qKlxuICAgICAqIFNob3cgdGhlIHBpY2tlciBpbiB0aGUgRE9NXG4gICAgICpcbiAgICAgKiBAcmV0dXJuIHt2b2lkfVxuICAgICAqL1xuICBzaG93KCkge1xuICAgIGNvbnN0IGlzTWlsaXRhcnlGb3JtYXQgPSB0aGlzLmlzTWlsaXRhcnlGb3JtYXQoKVxuXG4gICAgLy8gYmx1ciBpbnB1dCB0byBwcmV2ZW50IG9uc2NyZWVuIGtleWJvYXJkIGZyb20gZGlzcGxheWluZyAobW9iaWxlIGhhY2spXG4gICAgdGhpcy5pbnB1dEVsLmJsdXIoKVxuICAgIHRoaXMudG9nZ2xlSG91cnNWaXNpYmxlKHRydWUsIGlzTWlsaXRhcnlGb3JtYXQpXG4gICAgdGhpcy50b2dnbGVNaW51dGVzVmlzaWJsZSgpXG4gICAgdGhpcy5zZXREaXNwbGF5VGltZSh7XG4gICAgICBob3VyczogaXNNaWxpdGFyeUZvcm1hdCA/ICcwMCcgOiAnMTInLFxuICAgICAgbWludXRlczogJzAnLFxuICAgIH0pXG5cbiAgICB0aGlzLmNhY2hlZEVscy5ib2R5LnN0eWxlLm92ZXJmbG93ID0gJ2hpZGRlbidcbiAgICB0aGlzLmNhY2hlZEVscy5kaXNwbGF5TWVyaWRpZW0uc3R5bGUuZGlzcGxheSA9IGlzTWlsaXRhcnlGb3JtYXRcbiAgICAgID8gJ25vbmUnXG4gICAgICA6ICdpbmxpbmUnXG4gICAgdGhpcy5jYWNoZWRFbHMubWVyaWRpZW0uc3R5bGUuZGlzcGxheSA9IGlzTWlsaXRhcnlGb3JtYXQgPyAnbm9uZScgOiAnYmxvY2snXG4gICAgdGhpcy5jYWNoZWRFbHMub3ZlcmxheS5zdHlsZS5kaXNwbGF5ID0gJ2Jsb2NrJ1xuICAgIHRoaXMuY2FjaGVkRWxzLmNsb2NrSGFuZC5zdHlsZS5oZWlnaHQgPSBpc01pbGl0YXJ5Rm9ybWF0ID8gJzkwcHgnIDogJzEwNXB4J1xuXG4gICAgdGhpcy5ldmVudHMudHJpZ2dlcignc2hvdycpXG4gIH1cblxuICAvKipcbiAgICAgKiBFdmVudCBoYW5kbGUgZm9yIGlucHV0IGZvY3VzXG4gICAgICpcbiAgICAgKiBAcGFyYW0ge0V2ZW50fSBldmVudCBFdmVudCBvYmplY3QgcGFzc2VkIGZyb20gbGlzdGVuZXJcbiAgICAgKiBAcmV0dXJuIHt2b2lkfVxuICAgICAqL1xuICBzaG93RXZlbnQoZXZlbnQpIHtcbiAgICB0aGlzLmlucHV0RWwgPSBldmVudC50YXJnZXRcbiAgICB0aGlzLnNob3coKVxuICB9XG5cbiAgLyoqXG4gICAgICogSGlkZSB0aGUgcGlja2VyIGluIHRoZSBET01cbiAgICAgKlxuICAgICAqIEByZXR1cm4ge3ZvaWR9XG4gICAgICovXG4gIGhpZGUoKSB7XG4gICAgdGhpcy5jYWNoZWRFbHMub3ZlcmxheS5zdHlsZS5kaXNwbGF5ID0gJ25vbmUnXG4gICAgdGhpcy5jYWNoZWRFbHMuYm9keS5zdHlsZS5vdmVyZmxvdyA9ICcnXG5cbiAgICB0aGlzLmlucHV0RWwuZGlzcGF0Y2hFdmVudChuZXcgRXZlbnQoJ2JsdXInKSlcbiAgICB0aGlzLnJlc2V0U3RhdGUoKVxuICAgIHRoaXMuZXZlbnRzLnRyaWdnZXIoJ2hpZGUnKVxuICB9XG5cbiAgLyoqXG4gICAgICogSGlkZSB0aGUgcGlja2VyIGVsZW1lbnQgb24gdGhlIHBhZ2VcbiAgICAgKlxuICAgICAqIEBwYXJhbSB7RXZlbnR9IGV2ZW50IEV2ZW50IG9iamVjdCBwYXNzZWQgZnJvbSBldmVudCBsaXN0ZW5lciBjYWxsYmFja1xuICAgICAqIEByZXR1cm4ge3ZvaWR9XG4gICAgICovXG4gIGhpZGVFdmVudChldmVudCkge1xuICAgIGV2ZW50LnN0b3BQcm9wYWdhdGlvbigpXG5cbiAgICAvLyBvbmx5IGFsbG93IGV2ZW50IGJhc2VkIGNsb3NlIGlmIGV2ZW50LnRhcmdldCBjb250YWlucyBvbmUgb2YgdGhlc2UgY2xhc3Nlc1xuICAgIC8vIGhhY2sgdG8gcHJldmVudCBvdmVybGF5IGNsb3NlIGV2ZW50IGZyb20gZXZlbnRzLnRyaWdnZXJpbmcgb24gYWxsIGVsZW1lbnRzIGJlY2F1c2VcbiAgICAvLyB0aGV5IGFyZSBjaGlsZHJlbiBvZiBvdmVybGF5XG4gICAgY29uc3QgYWxsb3dlZENsYXNzZXMgPSBbJ210cC1vdmVybGF5JywgJ210cC1hY3Rpb25zX19jYW5jZWwnXVxuICAgIGNvbnN0IHsgY2xhc3NMaXN0IH0gPSBldmVudC50YXJnZXRcbiAgICBjb25zdCBpc0FsbG93ZWQgPSBhbGxvd2VkQ2xhc3Nlcy5zb21lKGFsbG93ZWRDbGFzcyA9PlxuICAgICAgY2xhc3NMaXN0LmNvbnRhaW5zKGFsbG93ZWRDbGFzcyksXG4gICAgKVxuXG4gICAgaWYgKGlzQWxsb3dlZCkge1xuICAgICAgdGhpcy5oaWRlKClcbiAgICB9XG4gIH1cblxuICAvKipcbiAgICAgKiBSZXNldCBwaWNrZXIgc3RhdGUgdG8gZGVmYXVsdHNcbiAgICAgKlxuICAgICAqIEByZXR1cm4ge3ZvaWR9XG4gICAgICovXG4gIHJlc2V0U3RhdGUoKSB7XG4gICAgdGhpcy5jdXJyZW50U3RlcCA9IDBcbiAgICB0aGlzLnRvZ2dsZUhvdXJzVmlzaWJsZSh0cnVlLCB0aGlzLmlzTWlsaXRhcnlGb3JtYXQoKSlcbiAgICB0aGlzLnRvZ2dsZU1pbnV0ZXNWaXNpYmxlKClcbiAgICB0aGlzLmNhY2hlZEVscy5jbG9ja0hvdXJzTGlbMF0uZGlzcGF0Y2hFdmVudChuZXcgRXZlbnQoJ2NsaWNrJykpXG4gICAgdGhpcy5jYWNoZWRFbHMuY2xvY2tNaW51dGVzTGlbMF0uZGlzcGF0Y2hFdmVudChuZXcgRXZlbnQoJ2NsaWNrJykpXG4gICAgdGhpcy5jYWNoZWRFbHMuY2xvY2tNaWxpdGFyeUhvdXJzTGlbMF0uZGlzcGF0Y2hFdmVudChuZXcgRXZlbnQoJ2NsaWNrJykpXG4gICAgdGhpcy5jYWNoZWRFbHMubWVyaWRpZW1TcGFuc1swXS5kaXNwYXRjaEV2ZW50KG5ldyBFdmVudCgnY2xpY2snKSlcbiAgfVxuXG4gIC8qKlxuICAgICAqIFNldCB0aGUgZGlzcGxheWVkIHRpbWUsIHdoaWNoIHdpbGwgYmUgdXNlZCB0byBmaWxsIGlucHV0IHZhbHVlIG9uIGNvbXBsZXRpb25cbiAgICAgKlxuICAgICAqIEBwYXJhbSB7bnVtYmVyfHN0cmluZ30gaG91cnM6IEhvdXIgZGlzcGxheSB0aW1lLFxuICAgICAqIEBwYXJhbSB7bnVtYmVyfHN0cmluZ30gbWludXRlczogTWludXRlIGRpc3BsYXkgdGltZVxuICAgICAqIEByZXR1cm4ge3ZvaWR9XG4gICAgICovXG4gIHNldERpc3BsYXlUaW1lKHsgaG91cnMsIG1pbnV0ZXMgfSkge1xuICAgIGlmIChob3Vycykge1xuICAgICAgLy8gLnRyaW0oKSBpcyBub3QgYWxsb3dlZCBpZiBob3VycyBpcyBub3QgcmVjb2duaXplZCBhcyBhIHN0cmluZyxcbiAgICAgIGlmICh0eXBlb2YgaG91cnMgPT09ICdzdHJpbmcnIHx8IGhvdXJzIGluc3RhbmNlb2YgU3RyaW5nKSB7XG4gICAgICAgIHRoaXMuY2FjaGVkRWxzLmRpc3BsYXlIb3Vycy5pbm5lckhUTUwgPSBob3Vycy50cmltKClcbiAgICAgIH0gZWxzZSB7XG4gICAgICAgIHRoaXMuY2FjaGVkRWxzLmRpc3BsYXlIb3Vycy5pbm5lckhUTUwgPSBob3Vyc1xuICAgICAgfVxuICAgIH1cbiAgICBpZiAobWludXRlcykge1xuICAgICAgY29uc3QgbWluID0gbWludXRlcyA8IDEwID8gYDAke21pbnV0ZXN9YCA6IG1pbnV0ZXNcblxuICAgICAgLy8gLnRyaW0oKSBpcyBub3QgYWxsb3dlZCBpZiBtaW4gaXMgbm90IHJlY29nbml6ZWQgYXMgYSBzdHJpbmcsXG4gICAgICAvLyAuLi4gc29tZXRpbWVzIChpbiBTYWZhcmkgYW5kIENocm9tZSkgaXQgaXMgYW4gdW50cmltbWFibGUgbnVtYmVyXG4gICAgICBpZiAodHlwZW9mIG1pbiA9PT0gJ3N0cmluZycgfHwgbWluIGluc3RhbmNlb2YgU3RyaW5nKSB7XG4gICAgICAgIHRoaXMuY2FjaGVkRWxzLmRpc3BsYXlNaW51dGVzLmlubmVySFRNTCA9IG1pbi50cmltKClcbiAgICAgIH0gZWxzZSB7XG4gICAgICAgIHRoaXMuY2FjaGVkRWxzLmRpc3BsYXlNaW51dGVzLmlubmVySFRNTCA9IG1pblxuICAgICAgfVxuICAgIH1cbiAgICBcbiAgICBjb25zdCBudW1lcmljSG91ciA9IHBhcnNlSW50KGhvdXJzKTtcbiAgICBjb25zdCBudW1lcmljTWludXRlID0gcGFyc2VJbnQobWludXRlcyk7XG4gICAgXG4gICAgXG4gIH1cblxuICAvKipcbiAgICAgKiBSb3RhdGUgdGhlIGhhbmQgZWxlbWVudCB0byBzZWxlY3RlZCB0aW1lXG4gICAgICpcbiAgICAgKiBAcGFyYW0ge251bWJlcn0gbm9kZUluZGV4IEluZGV4IG9mIGFjdGl2ZSBlbGVtZW50XG4gICAgICogQHBhcmFtIHtudW1iZXJ9IGluY3JlbWVudCBEZWdyZWUgaW5jcmVtZW50IGVsZW1lbnRzIGFyZSBvblxuICAgICAqIEByZXR1cm4ge3ZvaWR9XG4gICAgICovXG4gIHJvdGF0ZUhhbmQobm9kZUluZGV4ID0gOSwgaW5jcmVtZW50ID0gMzApIHtcbiAgICAvLyAwIGluZGV4IGlzIDE4MCBkZWdyZXNzIGJlaGluZCAwIGRlZ1xuICAgIGNvbnN0IHJvdGF0ZURlZyA9IG5vZGVJbmRleCAqIGluY3JlbWVudCAtIDE4MFxuICAgIGNvbnN0IHN0eWxlVmFsID0gYHJvdGF0ZSgke3JvdGF0ZURlZ31kZWcpYFxuXG4gICAgdGhpcy5jYWNoZWRFbHMuY2xvY2tIYW5kLnN0eWxlLnRyYW5zZm9ybSA9IHN0eWxlVmFsXG4gICAgdGhpcy5jYWNoZWRFbHMuY2xvY2tIYW5kLnN0eWxlWyctd2Via2l0LXRyYW5zZm9ybSddID0gc3R5bGVWYWxcbiAgICB0aGlzLmNhY2hlZEVscy5jbG9ja0hhbmQuc3R5bGVbJy1tcy10cmFuc2Zvcm0nXSA9IHN0eWxlVmFsXG4gIH1cblxuICBzaG93SG91cnMoKSB7XG4gICAgY29uc3QgaXNNaWxpdGFyeUZvcm1hdCA9IHRoaXMuaXNNaWxpdGFyeUZvcm1hdCgpXG4gICAgY29uc3QgaG91ckVscyA9IGlzTWlsaXRhcnlGb3JtYXRcbiAgICAgID8gdGhpcy5jYWNoZWRFbHMuY2xvY2tNaWxpdGFyeUhvdXJzTGlcbiAgICAgIDogdGhpcy5jYWNoZWRFbHMuY2xvY2tIb3Vyc0xpXG5cbiAgICB0aGlzLnRvZ2dsZUhvdXJzVmlzaWJsZSh0cnVlLCBpc01pbGl0YXJ5Rm9ybWF0KVxuICAgIHRoaXMudG9nZ2xlTWludXRlc1Zpc2libGUoKVxuICAgIHRoaXMucm90YXRlSGFuZCh0aGlzLmdldEFjdGl2ZUluZGV4KGhvdXJFbHMpKVxuICB9XG5cbiAgc2hvd01pbnV0ZXMoKSB7XG4gICAgY29uc3QgbWludXRlRWxzID0gdGhpcy5jYWNoZWRFbHMuY2xvY2tNaW51dGVzTGlcblxuICAgIHRoaXMudG9nZ2xlSG91cnNWaXNpYmxlKClcbiAgICB0aGlzLnRvZ2dsZU1pbnV0ZXNWaXNpYmxlKHRydWUpXG4gICAgdGhpcy5yb3RhdGVIYW5kKHRoaXMuZ2V0QWN0aXZlSW5kZXgobWludXRlRWxzKSwgNilcbiAgICB0aGlzLmNhY2hlZEVscy5jbG9ja0hhbmQuc3R5bGUuaGVpZ2h0ID0gJzExNXB4J1xuICB9XG5cbiAgZmluaXNoKCkge1xuICAgIHRoaXMudGltZVNlbGVjdGVkKClcbiAgICB0aGlzLmhpZGUoKVxuICB9XG5cbiAgLyoqXG4gICAgICogVG9nZ2xlIGhvdXIgKGJvdGggbWlsaXRhcnkgYW5kIHN0YW5kYXJkKSBjbG9jayB2aXNpYmxpdHkgaW4gRE9NXG4gICAgICpcbiAgICAgKiBAcGFyYW0ge2Jvb2xlYW59IGlzVmlzaWJsZSBJcyBjbG9jayBmYWNlIHRvZ2dsZWQgdmlzaWJsZSBvciBoaWRkZW5cbiAgICAgKiBAcGFyYW0ge2Jvb2xlYW59IGlzTWlsaXRhcnlGb3JtYXQgSXMgdXNpbmcgbWlsaXRhcnkgaG91ciBmb3JtYXRcbiAgICAgKiBAcmV0dXJuIHt2b2lkfVxuICAgICAqL1xuICB0b2dnbGVIb3Vyc1Zpc2libGUoaXNWaXNpYmxlID0gZmFsc2UsIGlzTWlsaXRhcnlGb3JtYXQgPSBmYWxzZSkge1xuICAgIHRoaXMuY2FjaGVkRWxzLmNsb2NrSG91cnMuc3R5bGUuZGlzcGxheSA9XG4gICAgICBpc1Zpc2libGUgJiYgIWlzTWlsaXRhcnlGb3JtYXQgPyAnYmxvY2snIDogJ25vbmUnXG4gICAgdGhpcy5jYWNoZWRFbHMuY2xvY2tNaWxpdGFyeUhvdXJzLnN0eWxlLmRpc3BsYXkgPVxuICAgICAgaXNWaXNpYmxlICYmIGlzTWlsaXRhcnlGb3JtYXQgPyAnYmxvY2snIDogJ25vbmUnXG4gICAgdGhpcy5jYWNoZWRFbHMuYnV0dG9uTmV4dC5zdHlsZS5kaXNwbGF5ID0gIWlzVmlzaWJsZVxuICAgICAgPyAnaW5saW5lLWJsb2NrJ1xuICAgICAgOiAnbm9uZSdcbiAgfVxuXG4gIC8qKlxuICAgICAqIFRvZ2dsZSBtaW51dGUgY2xvY2sgdmlzaWJsaXR5IGluIERPTVxuICAgICAqXG4gICAgICogQHBhcmFtIHtib29sZWFufSBpc1Zpc2libGUgSXMgY2xvY2sgZmFjZSB0b2dnbGVkIHZpc2libGUgb3IgaGlkZGVuXG4gICAgICogQHJldHVybiB7dm9pZH1cbiAgICAgKi9cbiAgdG9nZ2xlTWludXRlc1Zpc2libGUoaXNWaXNpYmxlID0gZmFsc2UpIHtcbiAgICB0aGlzLmNhY2hlZEVscy5jbG9ja01pbnV0ZXMuc3R5bGUuZGlzcGxheSA9IGlzVmlzaWJsZSA/ICdibG9jaycgOiAnbm9uZSdcbiAgICB0aGlzLmNhY2hlZEVscy5idXR0b25CYWNrLnN0eWxlLmRpc3BsYXkgPSBpc1Zpc2libGVcbiAgICAgID8gJ2lubGluZS1ibG9jaydcbiAgICAgIDogJ25vbmUnXG4gICAgdGhpcy5jYWNoZWRFbHMuYnV0dG9uTmV4dC5zdHlsZS5kaXNwbGF5ID0gIWlzVmlzaWJsZVxuICAgICAgPyAnaW5saW5lLWJsb2NrJ1xuICAgICAgOiAnbm9uZSdcbiAgICB0aGlzLmNhY2hlZEVscy5idXR0b25GaW5pc2guc3R5bGUuZGlzcGxheSA9IGlzVmlzaWJsZVxuICAgICAgPyAnaW5saW5lLWJsb2NrJ1xuICAgICAgOiAnbm9uZSdcbiAgfVxuXG4gIC8qKlxuICAgICAqIEdldCB0aGUgYWN0aXZlIHRpbWUgZWxlbWVudCBpbmRleFxuICAgICAqXG4gICAgICogQHBhcmFtIHtIVE1MQ29sbGVjdGlvbn0gdGltZUVscyBDb2xsZWN0aW9uIG9mIHRpbWUgZWxlbWVudHMgdG8gZmluZCBhY3RpdmUgaW5cbiAgICAgKiBAcmV0dXJuIHtudW1iZXJ9IEFjdGl2ZSBlbGVtZW50IGluZGV4XG4gICAgICovXG4gIGdldEFjdGl2ZUluZGV4KHRpbWVFbHMpIHtcbiAgICBsZXQgYWN0aXZlSW5kZXggPSAwXG4gICAgO1tdLnNvbWUuY2FsbCh0aW1lRWxzLCAodGltZUVsLCBpbmRleCkgPT4ge1xuICAgICAgaWYgKHRpbWVFbC5jbGFzc0xpc3QuY29udGFpbnMoJ210cC1jbG9jay0tYWN0aXZlJykpIHtcbiAgICAgICAgYWN0aXZlSW5kZXggPSBpbmRleFxuXG4gICAgICAgIHJldHVybiB0cnVlXG4gICAgICB9XG5cbiAgICAgIHJldHVybiBmYWxzZVxuICAgIH0pXG5cbiAgICByZXR1cm4gYWN0aXZlSW5kZXhcbiAgfVxuXG4gIC8qKlxuICAgICAqIFNldCBzZWxlY3RlZCB0aW1lIHRvIGlucHV0IGVsZW1lbnRcbiAgICAgKlxuICAgICAqIEByZXR1cm4ge3ZvaWR9XG4gICAgICovXG4gIHRpbWVTZWxlY3RlZCgpIHtcbiAgICBjb25zdCBob3VycyA9IHRoaXMuY2FjaGVkRWxzLmRpc3BsYXlIb3Vycy5pbm5lckhUTUxcbiAgICBjb25zdCBtaW51dGVzID0gdGhpcy5jYWNoZWRFbHMuZGlzcGxheU1pbnV0ZXMuaW5uZXJIVE1MXG4gICAgY29uc3QgbWVyaWRpZW0gPSB0aGlzLmlzTWlsaXRhcnlGb3JtYXQoKVxuICAgICAgPyAnJ1xuICAgICAgOiB0aGlzLmNhY2hlZEVscy5kaXNwbGF5TWVyaWRpZW0uaW5uZXJIVE1MXG4gICAgY29uc3QgdGltZVZhbHVlID0gYCR7aG91cnN9OiR7bWludXRlc30gJHttZXJpZGllbX1gXG5cbiAgICB0aGlzLmlucHV0RWwudmFsdWUgPSB0aW1lVmFsdWUudHJpbSgpXG4gICAgdGhpcy5pbnB1dEVsLmRpc3BhdGNoRXZlbnQobmV3IEV2ZW50KCdpbnB1dCcpKVxuICAgIHRoaXMuZXZlbnRzLnRyaWdnZXIoJ3RpbWVTZWxlY3RlZCcsIHtcbiAgICAgICAgaG91cnM6IGhvdXJzLFxuICAgICAgICBtaW51dGVzOiBtaW51dGVzLFxuICAgICAgICBtZXJpZGllbTogbWVyaWRpZW0sXG4gICAgICAgIHZhbHVlOiB0aW1lVmFsdWVcbiAgICB9KTtcbiAgfVxuXG4gIC8qKlxuICAgICAqIFNldCBhY3RpdmUgY2xvY2sgZmFjZSBlbGVtZW50XG4gICAgICpcbiAgICAgKiBAcGFyYW0ge0VsZW1lbnR9IGNvbnRhaW5lckVsIE5ldyBhY3RpdmUgZWxlbWVudHMgLnBhcmVudE5vZGVcbiAgICAgKiBAcGFyYW0ge0VsZW1lbnR9IGFjdGl2ZUVsIEVsZW1lbnQgdG8gc2V0IGFjdGl2ZVxuICAgICAqIEByZXR1cm4ge3ZvaWR9XG4gICAgICovXG4gIHNldEFjdGl2ZUVsKGNvbnRhaW5lckVsLCBhY3RpdmVFbCkge1xuICAgIGNvbnN0IGFjdGl2ZUNsYXNzTmFtZSA9ICdtdHAtY2xvY2stLWFjdGl2ZSdcbiAgICBjb25zdCBjdXJyZW50QWN0aXZlID0gY29udGFpbmVyRWwuZ2V0RWxlbWVudHNCeUNsYXNzTmFtZShhY3RpdmVDbGFzc05hbWUpWzBdXG5cbiAgICBjdXJyZW50QWN0aXZlLmNsYXNzTGlzdC5yZW1vdmUoYWN0aXZlQ2xhc3NOYW1lKVxuICAgIGFjdGl2ZUVsLmNsYXNzTGlzdC5hZGQoYWN0aXZlQ2xhc3NOYW1lKVxuICB9XG5cbiAgLyoqXG4gICAgICogTWVyaWRpZW0gc2VsZWN0IGV2ZW50IGhhbmRsZXJcbiAgICAgKlxuICAgICAqIEBwYXJhbSB7RXZlbnR9IGV2ZW50IEV2ZW50IG9iamVjdCBwYXNzZWQgZnJvbSBsaXN0ZW5lclxuICAgICAqIEByZXR1cm4ge3ZvaWR9XG4gICAgICovXG4gIG1lcmlkaWVtU2VsZWN0RXZlbnQoZXZlbnQpIHtcbiAgICBjb25zdCBhY3RpdmVDbGFzc05hbWUgPSAnbXRwLWNsb2NrLS1hY3RpdmUnXG4gICAgY29uc3QgZWxlbWVudCA9IGV2ZW50LnRhcmdldFxuICAgIGNvbnN0IGN1cnJlbnRBY3RpdmUgPSB0aGlzLmNhY2hlZEVscy5tZXJpZGllbS5nZXRFbGVtZW50c0J5Q2xhc3NOYW1lKFxuICAgICAgYWN0aXZlQ2xhc3NOYW1lLFxuICAgIClbMF1cbiAgICBjb25zdCB2YWx1ZSA9IGVsZW1lbnQuaW5uZXJIVE1MXG5cbiAgICBpZiAoIWN1cnJlbnRBY3RpdmUuaXNFcXVhbE5vZGUoZWxlbWVudCkpIHtcbiAgICAgIGN1cnJlbnRBY3RpdmUuY2xhc3NMaXN0LnJlbW92ZShhY3RpdmVDbGFzc05hbWUpXG4gICAgICBlbGVtZW50LmNsYXNzTGlzdC5hZGQoYWN0aXZlQ2xhc3NOYW1lKVxuICAgICAgdGhpcy5jYWNoZWRFbHMuZGlzcGxheU1lcmlkaWVtLmlubmVySFRNTCA9IHZhbHVlXG4gICAgfVxuICB9XG5cbiAgLyoqXG4gICAgICogSG91ciBzZWxlY3QgZXZlbnQgaGFuZGxlclxuICAgICAqXG4gICAgICogQHBhcmFtIHtFdmVudH0gZXZlbnQgRXZlbnQgb2JqZWN0IHBhc3NlZCBmcm9tIGxpc3RlbmVyXG4gICAgICogQHBhcmFtIHtIVE1MRWxlbWVudH0gY29udGFpbmVyRWwgRWxlbWVudCBjb250YWluaW5nIHRpbWUgbGlzdCBlbGVtZW50c1xuICAgICAqIEBwYXJhbSB7SFRNTENvbGxlY3Rpb259IGxpc3RFbHMgQ29sbGVjdGlvbiBvZiBsaXN0IGVsZW1lbnRzXG4gICAgICogQHJldHVybiB7dm9pZH1cbiAgICAgKi9cbiAgaG91clNlbGVjdEV2ZW50KGV2ZW50LCBjb250YWluZXJFbCwgbGlzdEVscykge1xuICAgIGV2ZW50LnN0b3BQcm9wYWdhdGlvbigpXG5cbiAgICBjb25zdCBuZXdBY3RpdmUgPSBldmVudC50YXJnZXRcbiAgICBjb25zdCBwYXJlbnRFbCA9IG5ld0FjdGl2ZS5wYXJlbnRFbGVtZW50XG4gICAgY29uc3QgaXNJbm5lciA9IHBhcmVudEVsLmNsYXNzTGlzdC5jb250YWlucygnbXRwLWNsb2NrX19ob3Vycy0taW5uZXInKVxuXG4gICAgdGhpcy5jYWNoZWRFbHMuY2xvY2tIYW5kLnN0eWxlLmhlaWdodCA9IGlzSW5uZXIgPyAnOTBweCcgOiAnMTA1cHgnXG4gICAgdGhpcy5zZXRBY3RpdmVFbChjb250YWluZXJFbCwgbmV3QWN0aXZlKVxuXG4gICAgY29uc3QgYWN0aXZlSW5kZXggPSB0aGlzLmdldEFjdGl2ZUluZGV4KGxpc3RFbHMpXG5cbiAgICB0aGlzLnNldERpc3BsYXlUaW1lKHsgaG91cnM6IG5ld0FjdGl2ZS5pbm5lckhUTUwgfSlcbiAgICB0aGlzLnJvdGF0ZUhhbmQoYWN0aXZlSW5kZXgpXG4gICAgdGhpcy5ldmVudHMudHJpZ2dlcignaG91clNlbGVjdGVkJylcbiAgfVxuXG4gIC8qKlxuICAgICAqIEhvdXIgc2VsZWN0IGV2ZW50IGhhbmRsZXJcbiAgICAgKlxuICAgICAqIEBwYXJhbSB7RXZlbnR9IGV2ZW50IEV2ZW50IG9iamVjdCBwYXNzZWQgZnJvbSBsaXN0ZW5lclxuICAgICAqIEBwYXJhbSB7SFRNTEVsZW1lbnR9IGNvbnRhaW5lckVsIEVsZW1lbnQgY29udGFpbmluZyB0aW1lIGxpc3QgZWxlbWVudHNcbiAgICAgKiBAcGFyYW0ge0hUTUxDb2xsZWN0aW9ufSBsaXN0RWxzIENvbGxlY3Rpb24gb2YgbGlzdCBlbGVtZW50c1xuICAgICAqIEByZXR1cm4ge3ZvaWR9XG4gICAgICovXG4gIG1pbnV0ZVNlbGVjdEV2ZW50KGV2ZW50LCBjb250YWluZXJFbCwgbGlzdEVscykge1xuICAgIGV2ZW50LnN0b3BQcm9wYWdhdGlvbigpXG5cbiAgICBjb25zdCBuZXdBY3RpdmUgPSBldmVudC50YXJnZXRcblxuICAgIHRoaXMuc2V0QWN0aXZlRWwoY29udGFpbmVyRWwsIG5ld0FjdGl2ZSlcblxuICAgIGNvbnN0IGFjdGl2ZUluZGV4ID0gdGhpcy5nZXRBY3RpdmVJbmRleChsaXN0RWxzKVxuXG4gICAgdGhpcy5zZXREaXNwbGF5VGltZSh7IG1pbnV0ZXM6IGFjdGl2ZUluZGV4IH0pXG4gICAgdGhpcy5yb3RhdGVIYW5kKGFjdGl2ZUluZGV4LCA2KVxuICAgIHRoaXMuZXZlbnRzLnRyaWdnZXIoJ21pbnV0ZVNlbGVjdGVkJylcbiAgfVxuXG4gIC8qKlxuICAgICAqIENoZWNrIGlmIHBpY2tlciBzZXQgdG8gbWlsaXRhcnkgdGltZSBtb2RlXG4gICAgICpcbiAgICAgKiBAcmV0dXJuIHtib29sZWFufSBJcyBpbiBtaWxpdGFyeSB0aW1lIG1vZGVcbiAgICAgKi9cbiAgaXNNaWxpdGFyeUZvcm1hdCgpIHtcbiAgICByZXR1cm4gdGhpcy5pbnB1dEVsLm10cE9wdGlvbnMudGltZUZvcm1hdCA9PT0gJ21pbGl0YXJ5J1xuICB9XG5cbiAgLyoqXG4gICAgICogQ2hlY2sgaWYgcGlja2VyIG9iamVjdCBoYXMgYWxyZWFkeSBzZXQgZXZlbnRzIG9uIHBpY2tlciBlbGVtZW50c1xuICAgICAqXG4gICAgICogQHJldHVybiB7Ym9vbGVhbn0gSGFzIGV2ZW50cyBiZWVuIHNldCBvbiBwaWNrZXIgZWxlbWVudHNcbiAgICAgKi9cbiAgaGFzU2V0RXZlbnRzKCkge1xuICAgIHJldHVybiB0aGlzLmNhY2hlZEVscy53cmFwcGVyLmNsYXNzTGlzdC5jb250YWlucygnbXRwLWV2ZW50cy1zZXQnKVxuICB9XG5cbiAgLyoqXG4gICAgICogQ2hlY2sgaWYgdGVtcGxhdGUgaGFzIGFscmVhZHkgYmVlbiBhcHBlbmRlZCB0byBET01cbiAgICAgKlxuICAgICAqIEByZXR1cm4ge2Jvb2xlYW59IElzIHRlbXBsYXRlIGluIERPTVxuICAgICAqL1xuICBpc1RlbXBsYXRlSW5ET00oKSB7XG4gICAgcmV0dXJuIEJvb2xlYW4oZG9jdW1lbnQuZ2V0RWxlbWVudHNCeUNsYXNzTmFtZSgnbXRwLW92ZXJsYXknKVswXSlcbiAgfVxufVxuXG5leHBvcnQgZGVmYXVsdCBUaW1lUGlja2VyXG5cblxuXG4vLyBXRUJQQUNLIEZPT1RFUiAvL1xuLy8gLi9zcmMvanMvdGltZXBpY2tlci5qcyIsImNvbnN0IHRlbXBsYXRlID0gYFxuPGRpdiBjbGFzcz1cIm10cC1vdmVybGF5XCIgc3R5bGU9XCJkaXNwbGF5Om5vbmVcIj5cbiAgICA8ZGl2IGNsYXNzPVwibXRwLXdyYXBwZXJcIj5cbiAgICAgICAgPGRpdiBjbGFzcz1cIm10cC1kaXNwbGF5XCI+XG4gICAgICAgICAgICA8c3BhbiBjbGFzcz1cIm10cC1kaXNwbGF5X19ob3Vyc1wiPjEyPC9zcGFuPjo8c3BhbiBjbGFzcz1cIm10cC1kaXNwbGF5X19taW51dGVzXCI+MDA8L3NwYW4+XG4gICAgICAgICAgICA8c3BhbiBjbGFzcz1cIm10cC1kaXNwbGF5X19tZXJpZGllbVwiPmFtPC9zcGFuPlxuICAgICAgICA8L2Rpdj48IS0tIEVORCAubXRwLWRpc3BsYXkgLS0+XG4gICAgICAgIDxkaXYgY2xhc3M9XCJtdHAtcGlja2VyXCI+XG4gICAgICAgICAgICA8ZGl2IGNsYXNzPVwibXRwLW1lcmlkaWVtXCI+XG4gICAgICAgICAgICAgICAgPHNwYW4gY2xhc3M9XCJtdHAtY2xvY2stLWFjdGl2ZVwiPmFtPC9zcGFuPlxuICAgICAgICAgICAgICAgIDxzcGFuPnBtPC9zcGFuPlxuICAgICAgICAgICAgPC9kaXY+PCEtLSBFTkQgLm10cC1tZXJpZGllbSAtLT5cbiAgICAgICAgICAgIDxkaXYgY2xhc3M9XCJtdHAtY2xvY2tcIj5cbiAgICAgICAgICAgICAgICA8ZGl2IGNsYXNzPVwibXRwLWNsb2NrX19jZW50ZXJcIj48L2Rpdj5cbiAgICAgICAgICAgICAgICA8ZGl2IGNsYXNzPVwibXRwLWNsb2NrX19oYW5kXCI+PC9kaXY+XG4gICAgICAgICAgICAgICAgPHVsIGNsYXNzPVwibXRwLWNsb2NrX190aW1lIG10cC1jbG9ja19fb3V0ZXIgbXRwLWNsb2NrX19ob3Vyc1wiIHN0eWxlPVwiZGlzcGxheTpub25lXCI+XG4gICAgICAgICAgICAgICAgICAgIDxsaSBjbGFzcz1cIm10cC1jbG9jay0tYWN0aXZlXCI+MTI8L2xpPlxuICAgICAgICAgICAgICAgICAgICA8bGk+MTwvbGk+XG4gICAgICAgICAgICAgICAgICAgIDxsaT4yPC9saT5cbiAgICAgICAgICAgICAgICAgICAgPGxpPjM8L2xpPlxuICAgICAgICAgICAgICAgICAgICA8bGk+NDwvbGk+XG4gICAgICAgICAgICAgICAgICAgIDxsaT41PC9saT5cbiAgICAgICAgICAgICAgICAgICAgPGxpPjY8L2xpPlxuICAgICAgICAgICAgICAgICAgICA8bGk+NzwvbGk+XG4gICAgICAgICAgICAgICAgICAgIDxsaT44PC9saT5cbiAgICAgICAgICAgICAgICAgICAgPGxpPjk8L2xpPlxuICAgICAgICAgICAgICAgICAgICA8bGk+MTA8L2xpPlxuICAgICAgICAgICAgICAgICAgICA8bGk+MTE8L2xpPlxuICAgICAgICAgICAgICAgIDwvdWw+XG4gICAgICAgICAgICAgICAgPHVsIGNsYXNzPVwibXRwLWNsb2NrX190aW1lIG10cC1jbG9ja19fb3V0ZXIgbXRwLWNsb2NrX19taW51dGVzXCIgc3R5bGU9XCJkaXNwbGF5Om5vbmVcIj5cbiAgICAgICAgICAgICAgICAgICAgPGxpIGNsYXNzPVwibXRwLWNsb2NrLS1hY3RpdmVcIj4wPC9saT5cbiAgICAgICAgICAgICAgICAgICAgPGxpPiZtaWRkb3Q7PC9saT5cbiAgICAgICAgICAgICAgICAgICAgPGxpPiZtaWRkb3Q7PC9saT5cbiAgICAgICAgICAgICAgICAgICAgPGxpPiZtaWRkb3Q7PC9saT5cbiAgICAgICAgICAgICAgICAgICAgPGxpPiZtaWRkb3Q7PC9saT5cbiAgICAgICAgICAgICAgICAgICAgPGxpPjU8L2xpPlxuICAgICAgICAgICAgICAgICAgICA8bGk+Jm1pZGRvdDs8L2xpPlxuICAgICAgICAgICAgICAgICAgICA8bGk+Jm1pZGRvdDs8L2xpPlxuICAgICAgICAgICAgICAgICAgICA8bGk+Jm1pZGRvdDs8L2xpPlxuICAgICAgICAgICAgICAgICAgICA8bGk+Jm1pZGRvdDs8L2xpPlxuICAgICAgICAgICAgICAgICAgICA8bGk+MTA8L2xpPlxuICAgICAgICAgICAgICAgICAgICA8bGk+Jm1pZGRvdDs8L2xpPlxuICAgICAgICAgICAgICAgICAgICA8bGk+Jm1pZGRvdDs8L2xpPlxuICAgICAgICAgICAgICAgICAgICA8bGk+Jm1pZGRvdDs8L2xpPlxuICAgICAgICAgICAgICAgICAgICA8bGk+Jm1pZGRvdDs8L2xpPlxuICAgICAgICAgICAgICAgICAgICA8bGk+MTU8L2xpPlxuICAgICAgICAgICAgICAgICAgICA8bGk+Jm1pZGRvdDs8L2xpPlxuICAgICAgICAgICAgICAgICAgICA8bGk+Jm1pZGRvdDs8L2xpPlxuICAgICAgICAgICAgICAgICAgICA8bGk+Jm1pZGRvdDs8L2xpPlxuICAgICAgICAgICAgICAgICAgICA8bGk+Jm1pZGRvdDs8L2xpPlxuICAgICAgICAgICAgICAgICAgICA8bGk+MjA8L2xpPlxuICAgICAgICAgICAgICAgICAgICA8bGk+Jm1pZGRvdDs8L2xpPlxuICAgICAgICAgICAgICAgICAgICA8bGk+Jm1pZGRvdDs8L2xpPlxuICAgICAgICAgICAgICAgICAgICA8bGk+Jm1pZGRvdDs8L2xpPlxuICAgICAgICAgICAgICAgICAgICA8bGk+Jm1pZGRvdDs8L2xpPlxuICAgICAgICAgICAgICAgICAgICA8bGk+MjU8L2xpPlxuICAgICAgICAgICAgICAgICAgICA8bGk+Jm1pZGRvdDs8L2xpPlxuICAgICAgICAgICAgICAgICAgICA8bGk+Jm1pZGRvdDs8L2xpPlxuICAgICAgICAgICAgICAgICAgICA8bGk+Jm1pZGRvdDs8L2xpPlxuICAgICAgICAgICAgICAgICAgICA8bGk+Jm1pZGRvdDs8L2xpPlxuICAgICAgICAgICAgICAgICAgICA8bGk+MzA8L2xpPlxuICAgICAgICAgICAgICAgICAgICA8bGk+Jm1pZGRvdDs8L2xpPlxuICAgICAgICAgICAgICAgICAgICA8bGk+Jm1pZGRvdDs8L2xpPlxuICAgICAgICAgICAgICAgICAgICA8bGk+Jm1pZGRvdDs8L2xpPlxuICAgICAgICAgICAgICAgICAgICA8bGk+Jm1pZGRvdDs8L2xpPlxuICAgICAgICAgICAgICAgICAgICA8bGk+MzU8L2xpPlxuICAgICAgICAgICAgICAgICAgICA8bGk+Jm1pZGRvdDs8L2xpPlxuICAgICAgICAgICAgICAgICAgICA8bGk+Jm1pZGRvdDs8L2xpPlxuICAgICAgICAgICAgICAgICAgICA8bGk+Jm1pZGRvdDs8L2xpPlxuICAgICAgICAgICAgICAgICAgICA8bGk+Jm1pZGRvdDs8L2xpPlxuICAgICAgICAgICAgICAgICAgICA8bGk+NDA8L2xpPlxuICAgICAgICAgICAgICAgICAgICA8bGk+Jm1pZGRvdDs8L2xpPlxuICAgICAgICAgICAgICAgICAgICA8bGk+Jm1pZGRvdDs8L2xpPlxuICAgICAgICAgICAgICAgICAgICA8bGk+Jm1pZGRvdDs8L2xpPlxuICAgICAgICAgICAgICAgICAgICA8bGk+Jm1pZGRvdDs8L2xpPlxuICAgICAgICAgICAgICAgICAgICA8bGk+NDU8L2xpPlxuICAgICAgICAgICAgICAgICAgICA8bGk+Jm1pZGRvdDs8L2xpPlxuICAgICAgICAgICAgICAgICAgICA8bGk+Jm1pZGRvdDs8L2xpPlxuICAgICAgICAgICAgICAgICAgICA8bGk+Jm1pZGRvdDs8L2xpPlxuICAgICAgICAgICAgICAgICAgICA8bGk+Jm1pZGRvdDs8L2xpPlxuICAgICAgICAgICAgICAgICAgICA8bGk+NTA8L2xpPlxuICAgICAgICAgICAgICAgICAgICA8bGk+Jm1pZGRvdDs8L2xpPlxuICAgICAgICAgICAgICAgICAgICA8bGk+Jm1pZGRvdDs8L2xpPlxuICAgICAgICAgICAgICAgICAgICA8bGk+Jm1pZGRvdDs8L2xpPlxuICAgICAgICAgICAgICAgICAgICA8bGk+Jm1pZGRvdDs8L2xpPlxuICAgICAgICAgICAgICAgICAgICA8bGk+NTU8L2xpPlxuICAgICAgICAgICAgICAgICAgICA8bGk+Jm1pZGRvdDs8L2xpPlxuICAgICAgICAgICAgICAgICAgICA8bGk+Jm1pZGRvdDs8L2xpPlxuICAgICAgICAgICAgICAgICAgICA8bGk+Jm1pZGRvdDs8L2xpPlxuICAgICAgICAgICAgICAgICAgICA8bGk+Jm1pZGRvdDs8L2xpPlxuICAgICAgICAgICAgICAgIDwvdWw+XG4gICAgICAgICAgICAgICAgPHVsIGNsYXNzPVwibXRwLWNsb2NrX190aW1lIG10cC1jbG9ja19faG91cnMtbWlsaXRhcnlcIiBzdHlsZT1cImRpc3BsYXk6bm9uZVwiPlxuICAgICAgICAgICAgICAgICAgICA8ZGl2IGNsYXNzPVwibXRwLWNsb2NrX19ob3Vycy0taW5uZXJcIj5cbiAgICAgICAgICAgICAgICAgICAgICAgIDxsaSBjbGFzcz1cIm10cC1jbG9jay0tYWN0aXZlXCI+MDA8L2xpPlxuICAgICAgICAgICAgICAgICAgICAgICAgPGxpPjEzPC9saT5cbiAgICAgICAgICAgICAgICAgICAgICAgIDxsaT4xNDwvbGk+XG4gICAgICAgICAgICAgICAgICAgICAgICA8bGk+MTU8L2xpPlxuICAgICAgICAgICAgICAgICAgICAgICAgPGxpPjE2PC9saT5cbiAgICAgICAgICAgICAgICAgICAgICAgIDxsaT4xNzwvbGk+XG4gICAgICAgICAgICAgICAgICAgICAgICA8bGk+MTg8L2xpPlxuICAgICAgICAgICAgICAgICAgICAgICAgPGxpPjE5PC9saT5cbiAgICAgICAgICAgICAgICAgICAgICAgIDxsaT4yMDwvbGk+XG4gICAgICAgICAgICAgICAgICAgICAgICA8bGk+MjE8L2xpPlxuICAgICAgICAgICAgICAgICAgICAgICAgPGxpPjIyPC9saT5cbiAgICAgICAgICAgICAgICAgICAgICAgIDxsaT4yMzwvbGk+XG4gICAgICAgICAgICAgICAgICAgIDwvZGl2PlxuICAgICAgICAgICAgICAgICAgICA8ZGl2IGNsYXNzPVwibXRwLWNsb2NrX19ob3Vyc1wiPlxuICAgICAgICAgICAgICAgICAgICAgICAgPGxpPjEyPC9saT5cbiAgICAgICAgICAgICAgICAgICAgICAgIDxsaT4xPC9saT5cbiAgICAgICAgICAgICAgICAgICAgICAgIDxsaT4yPC9saT5cbiAgICAgICAgICAgICAgICAgICAgICAgIDxsaT4zPC9saT5cbiAgICAgICAgICAgICAgICAgICAgICAgIDxsaT40PC9saT5cbiAgICAgICAgICAgICAgICAgICAgICAgIDxsaT41PC9saT5cbiAgICAgICAgICAgICAgICAgICAgICAgIDxsaT42PC9saT5cbiAgICAgICAgICAgICAgICAgICAgICAgIDxsaT43PC9saT5cbiAgICAgICAgICAgICAgICAgICAgICAgIDxsaT44PC9saT5cbiAgICAgICAgICAgICAgICAgICAgICAgIDxsaT45PC9saT5cbiAgICAgICAgICAgICAgICAgICAgICAgIDxsaT4xMDwvbGk+XG4gICAgICAgICAgICAgICAgICAgICAgICA8bGk+MTE8L2xpPlxuICAgICAgICAgICAgICAgICAgICA8L2Rpdj5cbiAgICAgICAgICAgICAgICA8L3VsPlxuICAgICAgICAgICAgPC9kaXY+PCEtLSBFTkQgLm10cC1jbG9jayAtLT5cbiAgICAgICAgICAgIDxkaXYgY2xhc3M9XCJtdHAtYWN0aW9uc1wiPlxuICAgICAgICAgICAgICAgIDxidXR0b24gdHlwZT1cImJ1dHRvblwiIGNsYXNzPVwibXRwLWFjdGlvbnNfX2J1dHRvbiBtdHAtYWN0aW9uc19fY2FuY2VsXCI+Q2FuY2VsPC9idXR0b24+XG4gICAgICAgICAgICAgICAgPGJ1dHRvbiB0eXBlPVwiYnV0dG9uXCIgY2xhc3M9XCJtdHAtYWN0aW9uc19fYnV0dG9uIG10cC1hY3Rpb25zX19iYWNrXCIgc3R5bGU9XCJkaXNwbGF5Om5vbmVcIj5CYWNrPC9idXR0b24+XG4gICAgICAgICAgICAgICAgPGJ1dHRvbiB0eXBlPVwiYnV0dG9uXCIgY2xhc3M9XCJtdHAtYWN0aW9uc19fYnV0dG9uIG10cC1hY3Rpb25zX19uZXh0XCI+TmV4dDwvYnV0dG9uPlxuICAgICAgICAgICAgICAgIDxidXR0b24gdHlwZT1cImJ1dHRvblwiIGNsYXNzPVwibXRwLWFjdGlvbnNfX2J1dHRvbiBtdHAtYWN0aW9uc19fZmluaXNoXCIgc3R5bGU9XCJkaXNwbGF5Om5vbmVcIj5Eb25lPC9idXR0b24+XG4gICAgICAgICAgICA8L2Rpdj48IS0tIEVORCAubXRwLWFjdGlvbnMgLS0+XG4gICAgICAgIDwvZGl2PjwhLS0gRU5EIC5tdHAtcGlja2VyIC0tPlxuICAgIDwvZGl2PjwhLS0gRU5EIC5tdHAtd3JhcHBlciAtLT5cbjwvZGl2PjwhLS0gRU5EIC5tdHAtb3ZlcmxheSAtLT5cbmBcblxuZXhwb3J0IGRlZmF1bHQgdGVtcGxhdGVcblxuXG5cbi8vIFdFQlBBQ0sgRk9PVEVSIC8vXG4vLyAuL3NyYy9qcy90ZW1wbGF0ZS5qcyIsIi8qIGVzbGludC1kaXNhYmxlIG5vLWNvbnRpbnVlICovXG4vKipcbiAqIE9iamVjdC5hc3NpZ24gcG9seWZpbGxcbiAqXG4gKiBAcGFyYW0ge29iamVjdH0gdGFyZ2V0IFRhcmdldCBvYmplY3QgdG8gbWVyZ2UgcHJvcGVydGllcyBvbnRvXG4gKiBAcGFyYW0gey4uLm9iamVjdH0gc291cmNlcyAgU291cmNlIG9iamVjdCB0byBtZXJnZSBwcm9wZXJ0aWVzIGZyb21cbiAqIEByZXR1cm4ge29iamVjdH0gVGFyZ2V0IG9iamVjdCB3aXRoIG1lcmdlZCBwcm9wZXJ0aWVzXG4gKi9cbmZ1bmN0aW9uIGFzc2lnbih0YXJnZXQsIC4uLnNvdXJjZXMpIHtcbiAgaWYgKHRhcmdldCA9PT0gJ3VuZGVmaW5lZCcgfHwgdGFyZ2V0ID09PSBudWxsKSB7XG4gICAgdGhyb3cgbmV3IFR5cGVFcnJvcignQ2Fubm90IGNvbnZlcnQgZmlyc3QgYXJndW1lbnQgdG8gb2JqZWN0JylcbiAgfVxuXG4gIGNvbnN0IHRvID0gT2JqZWN0KHRhcmdldClcblxuICBmb3IgKGxldCBpbmMgPSAwOyBpbmMgPCBzb3VyY2VzLmxlbmd0aDsgaW5jICs9IDEpIHtcbiAgICBsZXQgbmV4dFNvdXJjZSA9IHNvdXJjZXNbaW5jXVxuXG4gICAgaWYgKG5leHRTb3VyY2UgPT09ICd1bmRlZmluZWQnIHx8IG5leHRTb3VyY2UgPT09IG51bGwpIHtcbiAgICAgIGNvbnRpbnVlXG4gICAgfVxuXG4gICAgbmV4dFNvdXJjZSA9IE9iamVjdChuZXh0U291cmNlKVxuXG4gICAgY29uc3Qga2V5c0FycmF5ID0gT2JqZWN0LmtleXMobmV4dFNvdXJjZSlcblxuICAgIGZvciAoXG4gICAgICBsZXQgbmV4dEluZGV4ID0gMCwgbGVuID0ga2V5c0FycmF5Lmxlbmd0aDtcbiAgICAgIG5leHRJbmRleCA8IGxlbjtcbiAgICAgIG5leHRJbmRleCArPSAxXG4gICAgKSB7XG4gICAgICBjb25zdCBuZXh0S2V5ID0ga2V5c0FycmF5W25leHRJbmRleF1cbiAgICAgIGNvbnN0IGRlc2MgPSBPYmplY3QuZ2V0T3duUHJvcGVydHlEZXNjcmlwdG9yKG5leHRTb3VyY2UsIG5leHRLZXkpXG5cbiAgICAgIGlmIChkZXNjICE9PSAndW5kZWZpbmVkJyAmJiBkZXNjLmVudW1lcmFibGUpIHtcbiAgICAgICAgdG9bbmV4dEtleV0gPSBuZXh0U291cmNlW25leHRLZXldXG4gICAgICB9XG4gICAgfVxuICB9XG5cbiAgcmV0dXJuIHRvXG59XG5cbmV4cG9ydCBkZWZhdWx0IGFzc2lnblxuXG5cblxuLy8gV0VCUEFDSyBGT09URVIgLy9cbi8vIC4vc3JjL2pzL2Fzc2lnbi5qcyIsIi8qKlxuICogQGNsYXNzIEV2ZW50c1xuICpcbiAqIEBwcm9wIHtvYmplY3QuPHN0cmluZyxmdW5jdGlvbj59IGV2ZW50cyAtIEhhc2ggdGFibGUgb2YgZXZlbnRzIGFuZCB0aGVpciBhc3NpZ25lZCBoYW5kbGVyIGNhbGxiYWNrc1xuICovXG5leHBvcnQgZGVmYXVsdCBjbGFzcyBFdmVudHMge1xuICBldmVudHMgPSB7fVxuXG4gIC8qKlxuICAgICAqIFNldCBoYW5kbGVyIG9uIGV2ZW50XG4gICAgICpcbiAgICAgKiBAcGFyYW0ge3N0cmluZ30gZXZlbnQgLSBFdmVudCBuYW1lIHRvIHNldCBoYW5kbGVyIHRvXG4gICAgICogQHBhcmFtIHtmdW5jfSBoYW5kbGVyIC0gSGFuZGxlciBmdW5jdGlvbiBjYWxsYmFja1xuICAgICAqIEByZXR1cm4ge3ZvaWR9XG4gICAgICovXG4gIG9uKGV2ZW50LCBoYW5kbGVyKSB7XG4gICAgaWYgKCF0aGlzLmV2ZW50c1tldmVudF0pIHtcbiAgICAgIHRoaXMuZXZlbnRzW2V2ZW50XSA9IFtdXG4gICAgfVxuXG4gICAgdGhpcy5ldmVudHNbZXZlbnRdLnB1c2goaGFuZGxlcilcbiAgfVxuXG4gIC8qKlxuICAgICAqIFJlbW92ZSBhbGwgZXZlbnQgaGFuZGxlciBmb3IgdGhlIGdpdmVuIGV2ZW50XG4gICAgICpcbiAgICAgKiBAcGFyYW0ge3N0cmluZ30gZXZlbnQgLSBFdmVudCBuYW1lIHRvIHJlbW92ZSBoYW5kbGVyIGZyb21cbiAgICAgKiBAcmV0dXJuIHt2b2lkfVxuICAgICAqL1xuICBvZmYoZXZlbnQpIHtcbiAgICBpZiAodGhpcy5ldmVudHNbZXZlbnRdKSB7XG4gICAgICB0aGlzLmV2ZW50c1tldmVudF0gPSBbXVxuICAgIH1cbiAgfVxuXG4gIC8qKlxuICAgICAqIFRyaWdnZXIgZXZlbnQgd2l0aCBwYXJhbXNcbiAgICAgKlxuICAgICAqIEBwYXJhbSB7c3RyaW5nfSBldmVudCAtIEV2ZW50IHRvIHRyaWdnZXJcbiAgICAgKiBAcGFyYW0ge29iamVjdH0gcGFyYW1zIC0gUGFyYW1ldGVycyB0byBwYXNzIHRvIGV2ZW50IGhhbmRsZXJcbiAgICAgKiBAcmV0dXJuIHt2b2lkfVxuICAgICAqL1xuICB0cmlnZ2VyKGV2ZW50LCBwYXJhbXMpIHtcbiAgICBpZiAodGhpcy5ldmVudHNbZXZlbnRdICYmIHRoaXMuZXZlbnRzW2V2ZW50XS5sZW5ndGgpIHtcbiAgICAgIHRoaXMuZXZlbnRzW2V2ZW50XS5mb3JFYWNoKGhhbmRsZXIgPT4gaGFuZGxlcihwYXJhbXMpKVxuICAgIH1cbiAgfVxufVxuXG5cblxuLy8gV0VCUEFDSyBGT09URVIgLy9cbi8vIC4vc3JjL2pzL2V2ZW50cy5qcyIsIi8vIHJlbW92ZWQgYnkgZXh0cmFjdC10ZXh0LXdlYnBhY2stcGx1Z2luXG5cblxuLy8vLy8vLy8vLy8vLy8vLy8vXG4vLyBXRUJQQUNLIEZPT1RFUlxuLy8gLi9zcmMvc2Fzcy9tYWluLnNjc3Ncbi8vIG1vZHVsZSBpZCA9IDVcbi8vIG1vZHVsZSBjaHVua3MgPSAwIl0sInNvdXJjZVJvb3QiOiIifQ==