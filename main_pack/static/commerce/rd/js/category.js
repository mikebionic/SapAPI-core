(window.webpackJsonp = window.webpackJsonp || []).push([[16], {
  279: function(t, e, r) {
      t.exports = {}
  },
  280: function(t, e, r) {
      "use strict";
      var n = {
          name: "Currency"
      }
        , o = (r(284),
      r(13))
        , component = Object(o.a)(n, (function() {
          var t = this
            , e = t.$createElement;
          t._self._c;
          return t._m(0)
      }
      ), [function() {
          var t = this
            , e = t.$createElement
            , r = t._self._c || e;
          return r("span", {
              staticClass: "currency"
          }, [r("span", {
              attrs: {
                  hidden: "hidden"
              }
          }, [t._v("\n    руб.\n  ")])])
      }
      ], !1, null, null, null);
      e.a = component.exports
  },
  284: function(t, e, r) {
      "use strict";
      r(279)
  },
  286: function(t, e, r) {
      "use strict";
      var n = r(13)
        , component = Object(n.a)({}, (function() {
          var t = this.$createElement
            , e = this._self._c || t;
          return e("svg", {
              attrs: {
                  width: "12",
                  height: "12",
                  viewBox: "0 0 12 12",
                  fill: "none",
                  xmlns: "http://www.w3.org/2000/svg"
              }
          }, [e("path", {
              attrs: {
                  d: "M1 11L6 6M11 1L6 6M6 6L11 11L1 1",
                  stroke: "rgba(0, 0, 0, 0.5)",
                  "stroke-width": "2"
              }
          })])
      }
      ), [], !1, null, null, null);
      e.a = component.exports
  },
  287: function(t, e, r) {
      "use strict";
      var n = r(278)
        , o = r(286)
        , c = {
          name: "Modal",
          components: {
              IconBase: n.a,
              IconCrossGray: o.a
          },
          props: {
              isFixedCloseButton: {
                  type: Boolean,
                  default: !1
              },
              maxWidth: {
                  type: String,
                  default: "none"
              },
              maxHeight: {
                  type: String,
                  default: "none"
              },
              fullScreen: {
                  type: Boolean,
                  default: !1
              },
              hasCloseButton: {
                  type: Boolean,
                  default: !1
              }
          },
          mounted() {
              "www.respublica.ru" !== window.location.hostname && "rpm.respublica.ru" !== window.location.hostname && "localhost" !== window.location.hostname || window.history.pushState(null, null, window.location.href);
              var t = ()=>{
                  this.$emit("close", !1)
              }
              ;
              window.addEventListener("popstate", t),
              this.$once("hook:destroyed", (()=>{
                  window.removeEventListener("popstate", t)
              }
              )),
              this.$store.commit("modal/OPEN_MODAL"),
              document.body.classList.add("popup-is-active")
          },
          destroyed() {
              this.$store.commit("modal/CLOSE_MODAL"),
              0 === this.$store.state.modal.counterOpenModals && document.body.classList.remove("popup-is-active")
          },
          methods: {
              handleClose() {
                  this.$emit("close"),
                  0 !== this.$store.state.modal.counterOpenModals && window.history.back()
              }
          }
      }
        , l = (r(320),
      r(13))
        , component = Object(l.a)(c, (function() {
          var t = this
            , e = t.$createElement
            , r = t._self._c || e;
          return r("portal", {
              attrs: {
                  to: "popups"
              }
          }, [r("div", {
              staticClass: "popup"
          }, [r("div", {
              staticClass: "popup-wrapper"
          }, [r("div", {
              staticClass: "popup-overlay",
              attrs: {
                  title: "Закрыть окно"
              },
              on: {
                  click: t.handleClose
              }
          }), t._v(" "), r("div", {
              staticClass: "popup-content",
              class: t.fullScreen ? "popup-content-fullscreen" : "",
              style: {
                  maxHeight: t.maxHeight,
                  maxWidth: t.maxWidth
              }
          }, [t.hasCloseButton ? r("button", {
              staticClass: "popup-close",
              class: {
                  fixed: t.isFixedCloseButton
              },
              attrs: {
                  title: "Закрыть окно"
              },
              on: {
                  click: t.handleClose
              }
          }, [r("IconBase", [r("IconCrossGray")], 1)], 1) : t._e(), t._v(" "), t._t("default")], 2)])])])
      }
      ), [], !1, null, "baad5032", null);
      e.a = component.exports
  },
  288: function(t, e, r) {
      t.exports = {}
  },
  316: function(t, e) {
      t.exports = "\t\n\v\f\r                　\u2028\u2029\ufeff"
  },
  320: function(t, e, r) {
      "use strict";
      r(288)
  },
  336: function(t, e, r) {
      (function(e) {
          var r = /^\s+|\s+$/g
            , n = /^[-+]0x[0-9a-f]+$/i
            , o = /^0b[01]+$/i
            , c = /^0o[0-7]+$/i
            , l = parseInt
            , h = "object" == typeof e && e && e.Object === Object && e
            , d = "object" == typeof self && self && self.Object === Object && self
            , _ = h || d || Function("return this")()
            , v = Object.prototype.toString
            , m = Math.max
            , C = Math.min
            , f = function() {
              return _.Date.now()
          };
          function y(t) {
              var e = typeof t;
              return !!t && ("object" == e || "function" == e)
          }
          function k(t) {
              if ("number" == typeof t)
                  return t;
              if (function(t) {
                  return "symbol" == typeof t || function(t) {
                      return !!t && "object" == typeof t
                  }(t) && "[object Symbol]" == v.call(t)
              }(t))
                  return NaN;
              if (y(t)) {
                  var e = "function" == typeof t.valueOf ? t.valueOf() : t;
                  t = y(e) ? e + "" : e
              }
              if ("string" != typeof t)
                  return 0 === t ? t : +t;
              t = t.replace(r, "");
              var h = o.test(t);
              return h || c.test(t) ? l(t.slice(2), h ? 2 : 8) : n.test(t) ? NaN : +t
          }
          t.exports = function(t, e, r) {
              var n, o, c, l, h, d, _ = 0, v = !1, w = !1, S = !0;
              if ("function" != typeof t)
                  throw new TypeError("Expected a function");
              function x(time) {
                  var e = n
                    , r = o;
                  return n = o = void 0,
                  _ = time,
                  l = t.apply(r, e)
              }
              function $(time) {
                  return _ = time,
                  h = setTimeout(O, e),
                  v ? x(time) : l
              }
              function M(time) {
                  var t = time - d;
                  return void 0 === d || t >= e || t < 0 || w && time - _ >= c
              }
              function O() {
                  var time = f();
                  if (M(time))
                      return I(time);
                  h = setTimeout(O, function(time) {
                      var t = e - (time - d);
                      return w ? C(t, c - (time - _)) : t
                  }(time))
              }
              function I(time) {
                  return h = void 0,
                  S && n ? x(time) : (n = o = void 0,
                  l)
              }
              function E() {
                  var time = f()
                    , t = M(time);
                  if (n = arguments,
                  o = this,
                  d = time,
                  t) {
                      if (void 0 === h)
                          return $(d);
                      if (w)
                          return h = setTimeout(O, e),
                          x(d)
                  }
                  return void 0 === h && (h = setTimeout(O, e)),
                  l
              }
              return e = k(e) || 0,
              y(r) && (v = !!r.leading,
              c = (w = "maxWait"in r) ? m(k(r.maxWait) || 0, e) : c,
              S = "trailing"in r ? !!r.trailing : S),
              E.cancel = function() {
                  void 0 !== h && clearTimeout(h),
                  _ = 0,
                  n = d = o = h = void 0
              }
              ,
              E.flush = function() {
                  return void 0 === h ? l : I(f())
              }
              ,
              E
          }
      }
      ).call(this, r(28))
  },
  340: function(t, e, r) {
      t.exports = {}
  },
  345: function(t, e, r) {
      "use strict";
      var n = r(4)
        , o = r(347).trim;
      n({
          target: "String",
          proto: !0,
          forced: r(348)("trim")
      }, {
          trim: function() {
              return o(this)
          }
      })
  },
  347: function(t, e, r) {
      var n = r(19)
        , o = "[" + r(316) + "]"
        , c = RegExp("^" + o + o + "*")
        , l = RegExp(o + o + "*$")
        , h = function(t) {
          return function(e) {
              var r = String(n(e));
              return 1 & t && (r = r.replace(c, "")),
              2 & t && (r = r.replace(l, "")),
              r
          }
      };
      t.exports = {
          start: h(1),
          end: h(2),
          trim: h(3)
      }
  },
  348: function(t, e, r) {
      var n = r(10)
        , o = r(316);
      t.exports = function(t) {
          return n((function() {
              return !!o[t]() || "​᠎" != "​᠎"[t]() || o[t].name !== t
          }
          ))
      }
  },
  349: function(t, e, r) {
      "use strict";
      var n = {
          props: {
              icon: {
                  type: String,
                  default: ""
              }
          },
          computed: {
              svgClass() {
                  return "nr-svg-icon--" + this.icon
              },
              svgLink() {
                  return "#icon-" + this.icon
              }
          }
      }
        , o = (r(353),
      r(13))
        , component = Object(o.a)(n, (function() {
          var t = this
            , e = t.$createElement
            , r = t._self._c || e;
          return r("span", {
              staticClass: "nr-svg-icon",
              class: t.svgClass
          }, [r("svg", {
              staticClass: "nr-svg-icon__symbol"
          }, [r("use", {
              attrs: {
                  "xlink:href": t.svgLink
              }
          })])])
      }
      ), [], !1, null, "4f57910c", null);
      e.a = component.exports
  },
  353: function(t, e, r) {
      "use strict";
      r(340)
  },
  355: function(t, e, r) {
      "use strict";
      var n = r(13)
        , component = Object(n.a)({}, (function() {
          var t = this.$createElement
            , e = this._self._c || t;
          return e("svg", {
              attrs: {
                  width: "24",
                  height: "24",
                  viewBox: "0 0 24 24",
                  xmlns: "http://www.w3.org/2000/svg"
              }
          }, [e("path", {
              attrs: {
                  d: "m 12,0.5 c -2.7495796,0 -5,2.2504204 -5,5 L 7,6 3.5,6 l -1,17.5 19,0 L 20.5,6 19.554688,6 17,6 17,5.5 c 0,-2.7495916 -2.250451,-5 -5,-5 z m 0,2 c 1.668651,0 3,1.3313116 3,3 L 15,6 9,6 9,5.5 c 0,-1.6687004 1.3313,-3 3,-3 z M 5.3886719,8 7,8 l 0,2.5 2,0 0,-2.5 6,0 0,2.5 2,0 0,-2.5 1.611328,0 0.771484,13.5 -14.7656245,0 L 5.3886719,8 Z"
              }
          })])
      }
      ), [], !1, null, null, null);
      e.a = component.exports
  },
  357: function(t, e, r) {
      t.exports = {}
  },
  370: function(t, e, r) {
      "use strict";
      r(9),
      r(14),
      r(12);
      var n = {
          name: "AuthBlock",
          components: {
              SignInByEmail: ()=>r.e(27).then(r.bind(null, 976)),
              SignInByPhone: ()=>Promise.all([r.e(0), r.e(52)]).then(r.bind(null, 977)),
              SignUp: ()=>Promise.all([r.e(0), r.e(58)]).then(r.bind(null, 978))
          },
          data: ()=>({
              currentSign: "SignInByEmail"
          }),
          computed: {
              currentSignComponent() {
                  return this.currentSign
              }
          },
          methods: {
              close() {
                  this.$emit("closeAuth")
              },
              changeAuthentication(t) {
                  this.currentSign = t
              }
          }
      }
        , o = (r(373),
      r(13))
        , component = Object(o.a)(n, (function() {
          var t = this
            , e = t.$createElement
            , r = t._self._c || e;
          return r("div", {
              staticClass: "authentication"
          }, [r("transition", {
              attrs: {
                  name: "fade",
                  mode: "out-in"
              }
          }, [r(t.currentSignComponent, {
              tag: "component",
              on: {
                  changeAuthentication: t.changeAuthentication,
                  close: t.close
              }
          })], 1)], 1)
      }
      ), [], !1, null, "3163365b", null);
      e.a = component.exports
  },
  373: function(t, e, r) {
      "use strict";
      r(357)
  },
  382: function(t, e, r) {
      t.exports = r.p + "img/logo.f3de1a2.svg"
  },
  389: function(t, e, r) {
      "use strict";
      var n = r(13)
        , component = Object(n.a)({}, (function() {
          var t = this.$createElement
            , e = this._self._c || t;
          return e("svg", {
              attrs: {
                  width: "26",
                  height: "26",
                  viewBox: "0 0 26 26",
                  xmlns: "http://www.w3.org/2000/svg"
              }
          }, [e("path", {
              attrs: {
                  d: "m 11.61621,2.1396485 c -4.8709529,0 -8.8164053,3.8296952 -8.8164054,8.5000005 0,4.670331 3.9454571,8.499999 8.8164054,8.499999 2.065444,0 3.9605,-0.694436 5.462891,-1.84375 l 4.734375,4.564453 1.386719,-1.441406 -4.679688,-4.511718 c 1.194434,-1.452054 1.91211,-3.281801 1.91211,-5.267578 0,-4.6703134 -3.945513,-8.5000005 -8.816407,-8.5000005 z m 0,2 c 3.831508,0 6.816407,2.9541729 6.816407,6.5000005 0,1.446306 -0.503468,2.789804 -1.351563,3.878906 l -0.103515,-0.09961 -1.388672,1.441406 0.03711,0.03516 c -1.117968,0.777408 -2.495064,1.244137 -4.009767,1.244137 -3.8315889,0 -6.8164054,-2.95413 -6.8164054,-6.499999 0,-3.5458357 2.9848211,-6.5000005 6.8164054,-6.5000005 z"
              }
          })])
      }
      ), [], !1, null, null, null);
      e.a = component.exports
  },
  400: function(t, e, r) {
      "use strict";
      var n = r(13)
        , component = Object(n.a)({}, (function() {
          var t = this.$createElement
            , e = this._self._c || t;
          return e("svg", {
              attrs: {
                  width: "20",
                  height: "20",
                  viewBox: "0 0 20 20",
                  xmlns: "http://www.w3.org/2000/svg"
              }
          }, [e("path", {
              attrs: {
                  d: "M 5.4140625,4 4,5.4140625 8.3632812,9.7773438 4,14.142578 5.4140625,15.556641 9.7773438,11.191406 14.142578,15.556641 15.556641,14.142578 11.191406,9.7773438 15.556641,5.4140625 14.142578,4 9.7773438,8.3632812 5.4140625,4 Z"
              }
          })])
      }
      ), [], !1, null, null, null);
      e.a = component.exports
  },
  421: function(t, e, r) {
      "use strict";
      var n = r(13)
        , component = Object(n.a)({}, (function() {
          var t = this.$createElement
            , e = this._self._c || t;
          return e("svg", {
              attrs: {
                  width: "8",
                  height: "5",
                  viewBox: "0 0 8 5",
                  xmlns: "http://www.w3.org/2000/svg"
              }
          }, [e("path", {
              attrs: {
                  d: "M 1.3535156,0.46875 0.64648438,1.1777344 4,4.53125 7.3535156,1.1777344 6.6464844,0.46875 4,3.1152344 1.3535156,0.46875 Z"
              }
          })])
      }
      ), [], !1, null, null, null);
      e.a = component.exports
  },
  593: function(t, e, r) {
      t.exports = {}
  },
  594: function(t, e, r) {
      t.exports = {}
  },
  595: function(t, e, r) {
      t.exports = {}
  },
  596: function(t, e, r) {
      t.exports = {}
  },
  597: function(t, e, r) {
      t.exports = {}
  },
  598: function(t, e, r) {
      t.exports = {}
  },
  599: function(t, e, r) {
      t.exports = {}
  },
  600: function(t, e, r) {
      t.exports = {}
  },
  601: function(t, e, r) {
      t.exports = {}
  },
  889: function(t, e, r) {
      "use strict";
      r(593)
  },
  890: function(t, e, r) {
      "use strict";
      r(594)
  },
  891: function(t, e, r) {
      "use strict";
      r(595)
  },
  892: function(t, e, r) {
      "use strict";
      r(596)
  },
  893: function(t, e, r) {
      "use strict";
      r(597)
  },
  894: function(t, e, r) {
      "use strict";
      r(598)
  },
  895: function(t, e, r) {
      "use strict";
      r(599)
  },
  896: function(t, e, r) {
      "use strict";
      r(600)
  },
  897: function(t, e, r) {
      "use strict";
      r(601)
  },
  928: function(t, e, r) {
      "use strict";
      r.r(e);
      var n = {
          name: "TheHeaderDesktopCategories",
          data: ()=>({
              selectedRootCategory: 1,
              maxCountSubChildren: 4
          }),
          computed: {
              categories() {
                  return this.$store.state.categories.items
              },
              childs() {
                  return this.categories.find((t=>t.id === this.selectedRootCategory)).childs
              },
              rootLinks() {
                  return this.categories.find((t=>t.id === this.selectedRootCategory)).links
              }
          },
          methods: {
              isShowDeepLink: (t,e)=>e < 5 - ((null == t ? void 0 : t.length) || 0),
              handleMouseEnter(t) {
                  this.selectedRootCategory = t
              },
              handleHide() {
                  this.$emit("hide")
              },
              computedClass(t) {
                  var e, r, n = (null === (e = t.childs) || void 0 === e ? void 0 : e.length) || 0, o = (null === (r = t.links) || void 0 === r ? void 0 : r.length) || 0;
                  return n + o > this.maxCountSubChildren ? "computed-span-5" : "computed-span-".concat(o + n)
              }
          }
      }
        , o = (r(889),
      r(13))
        , c = Object(o.a)(n, (function() {
          var t = this
            , e = t.$createElement
            , r = t._self._c || e;
          return r("div", {
              directives: [{
                  name: "click-outside",
                  rawName: "v-click-outside",
                  value: t.handleHide,
                  expression: "handleHide"
              }],
              staticClass: "catalog-menu-wrapper"
          }, [r("div", {
              staticClass: "catalog-menu nr-container"
          }, [r("div", {
              staticClass: "categories-root"
          }, [r("div", {
              staticClass: "category-root-items"
          }, t._l(t.categories, (function(e) {
              return r("nuxt-link", {
                  key: e.id,
                  staticClass: "category-root-item-link",
                  class: {
                      "root-item-selected": e.id === t.selectedRootCategory
                  },
                  attrs: {
                      to: "/" + e.cached_path
                  },
                  nativeOn: {
                      mouseenter: function(r) {
                          return t.handleMouseEnter(e.id)
                      },
                      click: function(e) {
                          return t.handleHide.apply(null, arguments)
                      }
                  }
              }, [t._v("\n          " + t._s(e.title) + "\n        ")])
          }
          )), 1)]), t._v(" "), r("div", {
              staticClass: "categories-children"
          }, [t._l(t.childs, (function(e) {
              return r("div", {
                  key: e.id,
                  staticClass: "category-children-item",
                  class: t.computedClass(e)
              }, [r("nuxt-link", {
                  staticClass: "child-header",
                  attrs: {
                      to: "/" + e.cached_path
                  },
                  nativeOn: {
                      click: function(e) {
                          return t.handleHide.apply(null, arguments)
                      }
                  }
              }, [t._v("\n          " + t._s(e.title) + "\n        ")]), t._v(" "), r("div", {
                  staticClass: "categories-sub-children"
              }, [t._l(e.childs, (function(e, n) {
                  return r("div", {
                      key: e.id,
                      staticClass: "category-sub-children-item"
                  }, [n < t.maxCountSubChildren ? r("nuxt-link", {
                      staticClass: "sub-child-header",
                      attrs: {
                          to: "/" + e.cached_path
                      },
                      nativeOn: {
                          click: function(e) {
                              return t.handleHide.apply(null, arguments)
                          }
                      }
                  }, [t._v("\n              " + t._s(e.title) + "\n            ")]) : t._e()], 1)
              }
              )), t._v(" "), t._l(e.links, (function(n, o) {
                  return r("div", {
                      key: n.id,
                      staticClass: "category-sub-children-item"
                  }, [t.isShowDeepLink(e.childs, o) ? r("a", {
                      staticClass: "sub-child-header",
                      attrs: {
                          href: n.link
                      }
                  }, [t._v("\n              " + t._s(n.title) + "\n            ")]) : t._e()])
              }
              )), t._v(" "), r("div", {
                  staticClass: "category-sub-children-item"
              }, [e.childs && e.childs.length > t.maxCountSubChildren ? r("nuxt-link", {
                  staticClass: "sub-child-header",
                  attrs: {
                      to: "/" + e.cached_path
                  },
                  nativeOn: {
                      click: function(e) {
                          return t.handleHide.apply(null, arguments)
                      }
                  }
              }, [t._v("\n              Еще " + t._s(e.childs.length - t.maxCountSubChildren) + "\n              "), r("svg", {
                  staticClass: "icons_corner-down",
                  attrs: {
                      viewBox: "0 0 24 24"
                  }
              }, [r("path", {
                  attrs: {
                      "fill-rule": "evenodd",
                      d: "M19.997 10.007L12 18.004l-7.997-7.997 1.414-1.414L12 15.176l6.583-6.583z",
                      fill: "#ccc"
                  }
              })])]) : t._e()], 1)], 2)], 1)
          }
          )), t._v(" "), t._l(t.rootLinks, (function(link) {
              return r("div", {
                  key: link.id,
                  staticClass: "category-children-item"
              }, [r("a", {
                  staticClass: "child-header",
                  attrs: {
                      href: link.link
                  }
              }, [t._v("\n          " + t._s(link.title) + "\n        ")])])
          }
          ))], 2)])])
      }
      ), [], !1, null, "dd976b0a", null).exports
        , l = r(278)
        , h = {
          name: "HeaderUserMenu",
          components: {
              IconUser: Object(o.a)({}, (function() {
                  var t = this.$createElement
                    , e = this._self._c || t;
                  return e("svg", {
                      attrs: {
                          width: "24",
                          height: "24",
                          viewBox: "0 0 24 24",
                          xmlns: "http://www.w3.org/2000/svg"
                      }
                  }, [e("path", {
                      attrs: {
                          d: "M 12 1 C 5.9367124 1 1 5.9367124 1 12 C 1 15.031644 2.2344735 17.781349 4.2265625 19.773438 C 6.2186515 21.765526 8.9683562 23 12 23 C 15.031644 23 17.781349 21.765525 19.773438 19.773438 C 21.765526 17.781349 23 15.031644 23 12 C 23 5.9367124 18.063288 1 12 1 z M 12 3 C 16.982407 3 21 7.0175926 21 12 C 21 14.154217 20.247535 16.127078 18.992188 17.673828 C 18.96422 17.638427 18.938077 17.601844 18.910156 17.566406 C 17.271549 15.486685 14.843983 14.0625 12 14.0625 C 9.1560172 14.0625 6.7284509 15.486685 5.0898438 17.566406 C 5.0619227 17.601844 5.0357794 17.638427 5.0078125 17.673828 C 3.752465 16.127078 3 14.154217 3 12 C 3 7.0175926 7.0175926 3 12 3 z M 12 5 C 9.8027056 5 8 6.8027056 8 9 C 8 11.197294 9.8027056 13 12 13 C 14.197294 13 16 11.197294 16 9 C 16 6.8027056 14.197294 5 12 5 z M 12 7 C 13.116414 7 14 7.8835859 14 9 C 14 10.116414 13.116414 11 12 11 C 10.883586 11 10 10.116414 10 9 C 10 7.8835859 10.883586 7 12 7 z M 12 16.0625 C 14.29957 16.0625 16.23326 17.243922 17.494141 18.957031 C 17.520996 18.993519 17.543819 19.031762 17.570312 19.068359 C 16.038937 20.275451 14.107963 21 12 21 C 9.892037 21 7.9610626 20.275451 6.4296875 19.068359 C 6.4561807 19.031762 6.479004 18.993519 6.5058594 18.957031 C 7.7667402 17.243922 9.7004301 16.0625 12 16.0625 z "
                      }
                  })])
              }
              ), [], !1, null, null, null).exports,
              IconBase: l.a
          },
          data: ()=>({
              isShowMenu: !1
          }),
          methods: {
              hideMenu() {
                  this.isShowMenu = !1
              },
              showAuth() {
                  this.$emit("showAuth")
              },
              signOut() {
                  this.$router.push("/"),
                  this.$store.dispatch("clearUser")
              }
          }
      }
        , d = (r(890),
      Object(o.a)(h, (function() {
          var t = this
            , e = t.$createElement
            , r = t._self._c || e;
          return r("div", {
              staticClass: "nr-header__user-nav-item nr-header__user-nav-item--user",
              class: {
                  "nr-header__user-nav-item--logged": t.$store.getters.currentUser
              }
          }, [t.$store.getters.currentUser ? r("div", {
              directives: [{
                  name: "click-outside",
                  rawName: "v-click-outside",
                  value: t.hideMenu,
                  expression: "hideMenu"
              }],
              staticClass: "nr-header__user-nav-link header-avatar",
              attrs: {
                  title: "Профиль"
              },
              on: {
                  click: function(e) {
                      t.isShowMenu = !t.isShowMenu
                  }
              }
          }, [r("span", {
              staticClass: "nr-avatar"
          }, ["" === t.$store.getters.currentUser.avatar.url || "/static/missing/avatar.png" === t.$store.getters.currentUser.avatar.url ? [t._v(t._s(t.$store.getters.currentUser.name.charAt(0)))] : [r("img", {
              staticClass: "nr-avatar-img",
              attrs: {
                  src: t.$store.getters.currentUser.avatar.url,
                  alt: "Аватар"
              }
          })], t._v(" "), t.isShowMenu ? r("div", {
              staticClass: "menu-list"
          }, [r("NuxtLink", {
              staticClass: "nr-header__user-nav-link menu-link",
              attrs: {
                  to: "/my/profile",
                  title: "Профиль"
              }
          }, [t._v("Профиль")]), t._v(" "), r("NuxtLink", {
              staticClass: "nr-header__user-nav-link menu-link",
              attrs: {
                  to: "/my/orders",
                  title: "Заказы"
              }
          }, [t._v("Заказы")]), t._v(" "), r("NuxtLink", {
              staticClass: "nr-header__user-nav-link menu-link",
              attrs: {
                  to: "/my/wishlist",
                  title: "Вишлист"
              }
          }, [t._v("Вишлист")]), t._v(" "), r("div", {
              staticClass: "nr-header__user-nav-link menu-link signout",
              attrs: {
                  title: "Выйти"
              },
              on: {
                  click: t.signOut
              }
          }, [t._v("\n          Выйти\n        ")]), t._v(" "), r("div", {
              staticClass: "arrow-top"
          })], 1) : t._e()], 2)]) : r("a", {
              staticClass: "nr-header__user-nav-link",
              attrs: {
                  href: "#",
                  title: "Авторизоваться"
              },
              on: {
                  click: function(e) {
                      return e.preventDefault(),
                      t.showAuth.apply(null, arguments)
                  }
              }
          }, [r("IconBase", {
              staticClass: "header-icon",
              attrs: {
                  "icon-name": "user"
              }
          }, [r("IconUser")], 1)], 1)])
      }
      ), [], !1, null, null, null).exports)
        , _ = {
          name: "HeaderMobileCategories",
          components: {
              SvgIcon: r(349).a
          },
          data: ()=>({
              selectedCategory: 0,
              selectedSubCategory: 0,
              subLinks: [{
                  title: "Lego в Республике*",
                  cached_path: "offers/lego-teper-v-respublike"
              }, {
                  title: "Акции",
                  cached_path: "promotions"
              }, {
                  title: "Скидки!",
                  cached_path: "sale"
              }, {
                  title: "Подборки",
                  cached_path: "lists"
              }, {
                  title: "Подарочный Сертификат",
                  cached_path: "podarki/podarochnye-sertifikaty-i-karty/467799-elektronnyy-podarochnyy-sertifikat"
              }, {
                  title: "Книжный абонемент",
                  cached_path: "podarki/podarochnye-sertifikaty-i-karty/519322-elektronnyi-knizhnyi-abonement"
              }, {
                  title: "Корпоративные продажи",
                  cached_path: "corp"
              }]
          }),
          computed: {
              categories() {
                  return this.$store.state.categories.items
              }
          },
          methods: {
              closeNav(t) {
                  this.$emit("hide"),
                  this.$router.push(t)
              },
              handleClickCategory(t) {
                  this.selectedSubCategory = 0,
                  this.selectedCategory === t ? this.selectedCategory = 0 : this.selectedCategory = t
              },
              handleClickSubCategory(t) {
                  this.selectedSubCategory === t ? this.selectedSubCategory = 0 : this.selectedSubCategory = t
              }
          }
      }
        , v = (r(891),
      {
          components: {
              HeaderMobileCategories: Object(o.a)(_, (function() {
                  var t = this
                    , e = t.$createElement
                    , r = t._self._c || e;
                  return r("div", {
                      staticClass: "nr-header__mobile-nav-block"
                  }, [r("ul", {
                      staticClass: "nr-header__accordion-nav",
                      class: {
                          "nr-header__accordion-nav--has-active": t.selectedCategory
                      }
                  }, [t._l(t.categories, (function(e) {
                      return r("li", {
                          key: "submobcat" + e.id,
                          staticClass: "nr-header__accordion-nav-item",
                          class: {
                              "nr-header__accordion-nav-item--active": t.selectedCategory === e.id
                          }
                      }, [e.childs ? r("a", {
                          staticClass: "nr-header__accordion-nav-link nr-header__accordion-nav-link--toggler",
                          attrs: {
                              title: e.title,
                              href: "#"
                          },
                          on: {
                              click: function(r) {
                                  return r.preventDefault(),
                                  t.handleClickCategory(e.id)
                              }
                          }
                      }, [t._v("\n        " + t._s(e.title) + "\n        "), r("SvgIcon", {
                          attrs: {
                              icon: "nr-triangle-down"
                          }
                      })], 1) : r("a", {
                          staticClass: "nr-header__accordion-nav-link nr-header__accordion-nav-link--toggler",
                          attrs: {
                              title: e.title,
                              href: "#"
                          },
                          on: {
                              click: function(r) {
                                  return r.preventDefault(),
                                  t.closeNav("/" + e.cached_path)
                              }
                          }
                      }, [t._v("\n        " + t._s(e.title) + "\n      ")]), t._v(" "), e.childs && t.selectedCategory === e.id ? r("ul", {
                          staticClass: "nr-header__accordion-nav",
                          class: {
                              "nr-header__accordion-nav--has-active": t.selectedSubCategory
                          }
                      }, [r("li", {
                          staticClass: "nr-header__accordion-nav-item"
                      }, [r("a", {
                          staticClass: "nr-header__accordion-nav-link",
                          attrs: {
                              href: "/" + e.cached_path,
                              title: "Все товары"
                          },
                          on: {
                              click: function(r) {
                                  return r.preventDefault(),
                                  t.closeNav("/" + e.cached_path)
                              }
                          }
                      }, [t._v("\n            Все товары\n          ")])]), t._v(" "), t._l(e.childs, (function(e) {
                          return r("li", {
                              key: "submobcat_" + e.id,
                              staticClass: "nr-header__accordion-nav-item",
                              class: {
                                  "nr-header__accordion-nav-item--active": t.selectedSubCategory === e.id
                              }
                          }, [e.childs || 0 !== e.links.length ? [r("a", {
                              staticClass: "\n                nr-header__accordion-nav-link\n                nr-header__accordion-nav-link--toggler\n              ",
                              attrs: {
                                  title: e.title,
                                  href: "#"
                              },
                              on: {
                                  click: function(r) {
                                      return r.preventDefault(),
                                      t.handleClickSubCategory(e.id)
                                  }
                              }
                          }, [t._v("\n              " + t._s(e.title) + "\n              "), r("SvgIcon", {
                              attrs: {
                                  icon: "nr-triangle-down"
                              }
                          })], 1), t._v(" "), e.childs || e.links ? r("ul", {
                              staticClass: "nr-header__accordion-nav"
                          }, [r("li", {
                              staticClass: "nr-header__accordion-nav-item"
                          }, [r("a", {
                              staticClass: "nr-header__accordion-nav-link",
                              attrs: {
                                  href: "/" + e.cached_path,
                                  title: "Все товары"
                              },
                              on: {
                                  click: function(r) {
                                      return r.preventDefault(),
                                      t.closeNav("/" + e.cached_path)
                                  }
                              }
                          }, [t._v("\n                  Все товары\n                ")])]), t._v(" "), t._l(e.childs, (function(e) {
                              return r("li", {
                                  key: "subsubmobcat_" + e.id,
                                  staticClass: "nr-header__accordion-nav-item"
                              }, [r("a", {
                                  staticClass: "nr-header__accordion-nav-link",
                                  attrs: {
                                      href: "/" + e.cached_path,
                                      title: e.title
                                  },
                                  on: {
                                      click: function(r) {
                                          return r.preventDefault(),
                                          t.closeNav("/" + e.cached_path)
                                      }
                                  }
                              }, [t._v("\n                  " + t._s(e.title) + "\n                ")])])
                          }
                          )), t._v(" "), t._l(e.links, (function(e) {
                              return r("li", {
                                  key: "subsubmobcatlinks_" + e.id,
                                  staticClass: "nr-header__accordion-nav-item"
                              }, [r("a", {
                                  staticClass: "nr-header__accordion-nav-link",
                                  attrs: {
                                      href: e.link,
                                      title: e.title
                                  }
                              }, [t._v("\n                  " + t._s(e.title) + "\n                ")])])
                          }
                          ))], 2) : t._e()] : r("a", {
                              staticClass: "nr-header__accordion-nav-link",
                              attrs: {
                                  href: "/" + e.cached_path,
                                  title: e.title
                              },
                              on: {
                                  click: function(r) {
                                      return r.preventDefault(),
                                      t.closeNav("/" + e.cached_path)
                                  }
                              }
                          }, [t._v("\n            " + t._s(e.title) + "\n          ")])], 2)
                      }
                      )), t._v(" "), t._l(e.links, (function(e) {
                          return r("li", {
                              key: "submobcatlinks_" + e.id,
                              staticClass: "nr-header__accordion-nav-item"
                          }, [r("a", {
                              staticClass: "nr-header__accordion-nav-link",
                              attrs: {
                                  href: e.link,
                                  title: e.title
                              }
                          }, [t._v("\n            " + t._s(e.title) + "\n          ")])])
                      }
                      ))], 2) : t._e()])
                  }
                  )), t._v(" "), r("div", {
                      staticClass: "nr-header__mobile-nav-block--top-border"
                  }, t._l(t.subLinks, (function(link, e) {
                      return r("li", {
                          key: "link_" + e,
                          staticClass: "nr-header__accordion-nav-item sub-links"
                      }, [r("a", {
                          staticClass: "\n            nr-header__accordion-nav-link\n            nr-header__accordion-nav-link--toggler\n          ",
                          attrs: {
                              href: "/" + link.cached_path,
                              title: link.title
                          },
                          on: {
                              click: function(e) {
                                  return e.preventDefault(),
                                  t.closeNav("/" + link.cached_path)
                              }
                          }
                      }, [t._v("\n          " + t._s(link.title) + "\n        ")])])
                  }
                  )), 0)], 2)])
              }
              ), [], !1, null, "7c0a3f58", null).exports
          },
          computed: {
              isAuth() {
                  return !!this.$store.getters.currentUser
              }
          },
          mounted() {
              document.body.classList.add("popup-is-active")
          },
          destroyed() {
              document.body.classList.remove("popup-is-active")
          },
          methods: {
              handleHide() {
                  this.$emit("hide")
              },
              handleClickAuth() {
                  this.$emit("showAuth")
              },
              userExit() {
                  this.$store.dispatch("clearUser"),
                  this.$emit("hide")
              }
          }
      })
        , m = (r(892),
      Object(o.a)(v, (function() {
          var t = this
            , e = t.$createElement
            , r = t._self._c || e;
          return r("div", {
              staticClass: "nr-header__mobile-nav"
          }, [t.isAuth ? r("div", {
              staticClass: "nr-header__mobile-nav-block"
          }, [r("div", {
              staticClass: "nr-header__mobile-nav-account"
          }, [r("nuxt-link", {
              staticClass: "nr-header__mobile-nav-account-avatar",
              attrs: {
                  to: "/my/orders"
              },
              nativeOn: {
                  click: function(e) {
                      return t.handleHide.apply(null, arguments)
                  }
              }
          }, [r("span", {
              staticClass: "nr-avatar"
          }, ["" === t.$store.state.currentUser.avatar.url || "/static/missing/avatar.png" === t.$store.state.currentUser.avatar.url ? [t._v(t._s(t.$store.state.currentUser.name.charAt(0)))] : [r("img", {
              staticClass: "nr-avatar-img",
              attrs: {
                  src: t.$store.state.currentUser.avatar.url,
                  alt: "Аватар"
              }
          })]], 2)]), t._v(" "), r("nuxt-link", {
              staticClass: "nr-header__mobile-nav-account-content",
              attrs: {
                  to: "/my/orders"
              },
              nativeOn: {
                  click: function(e) {
                      return t.handleHide.apply(null, arguments)
                  }
              }
          }, [t._v("\n        Мой аккаунт\n      ")]), t._v(" "), r("nuxt-link", {
              staticClass: "nr-header__mobile-nav-account-logout",
              attrs: {
                  to: "#",
                  title: "Выйти"
              },
              nativeOn: {
                  click: function(e) {
                      return t.userExit.apply(null, arguments)
                  }
              }
          }, [t._v("\n        Выйти\n      ")])], 1)]) : t._e(), t._v(" "), t.isAuth ? t._e() : r("div", {
              staticClass: "nr-header__mobile-nav-block"
          }, [r("a", {
              staticClass: "nr-header__mobile-nav-button",
              attrs: {
                  href: "#",
                  title: "Войти"
              },
              on: {
                  click: function(e) {
                      return e.preventDefault(),
                      t.handleClickAuth.apply(null, arguments)
                  }
              }
          }, [t._v("Войти")])]), t._v(" "), r("div", {
              staticClass: "nr-header__mobile-nav-block"
          }, [t.$store.state.currentUser ? r("nuxt-link", {
              staticClass: "nr-header__mobile-nav-button",
              attrs: {
                  to: "/my/wishlist",
                  title: "Вишлист"
              },
              nativeOn: {
                  click: function(e) {
                      return t.handleHide.apply(null, arguments)
                  }
              }
          }, [t._v("\n      Вишлист\n    ")]) : t._e()], 1), t._v(" "), r("HeaderMobileCategories", {
              on: {
                  hide: t.handleHide
              }
          }), t._v(" "), r("div", {
              staticClass: "\n      nr-header__mobile-nav-block nr-header__mobile-nav-block--top-border\n    "
          }, [r("ul", {
              staticClass: "nr-header__mobile-nav-links"
          }, [r("li", {
              staticClass: "nr-header__mobile-nav-links-item"
          }, [r("a", {
              staticClass: "nr-header__mobile-nav-link",
              attrs: {
                  href: "tel:" + t.$store.state.cityPhone
              }
          }, [t._v(t._s(t.$store.state.cityPhone))])]), t._v(" "), r("li", {
              staticClass: "nr-header__mobile-nav-links-item"
          }, [r("nuxt-link", {
              staticClass: "nr-header__mobile-nav-link",
              attrs: {
                  to: "/delivery/",
                  title: "Доставка и оплата"
              },
              nativeOn: {
                  click: function(e) {
                      return t.handleHide.apply(null, arguments)
                  }
              }
          }, [t._v("\n          Доставка и оплата\n        ")])], 1)])])], 1)
      }
      ), [], !1, null, null, null).exports)
        , C = {
          name: "TheHeaderCategories",
          data: ()=>({
              links: [{
                  title: "Lego в Республике*",
                  cached_path: "offers/lego-teper-v-respublike"
              }, {
                  title: "Акции",
                  cached_path: "promotions"
              }, {
                  title: "Скидки!",
                  cached_path: "sale"
              }, {
                  title: "Подборки",
                  cached_path: "lists"
              }, {
                  title: "Подарочный Сертификат",
                  cached_path: "podarki/podarochnye-sertifikaty-i-karty/467799-elektronnyy-podarochnyy-sertifikat"
              }, {
                  title: "Книжный абонемент",
                  cached_path: "podarki/podarochnye-sertifikaty-i-karty/519322-elektronnyi-knizhnyi-abonement"
              }, {
                  title: "Корпоративные продажи",
                  cached_path: "corp"
              }]
          })
      }
        , f = (r(893),
      Object(o.a)(C, (function() {
          var t = this
            , e = t.$createElement
            , r = t._self._c || e;
          return r("nav", {
              staticClass: "nr-header__nav",
              attrs: {
                  itemscope: "",
                  itemtype: "http://schema.org/SiteNavigationElement"
              }
          }, [r("ul", {
              staticClass: "nr-header__nav-list"
          }, t._l(t.links, (function(link) {
              return r("li", {
                  key: "links" + link.cached_path,
                  staticClass: "nr-header__nav-item submenu-item",
                  attrs: {
                      itemprop: "name"
                  }
              }, [r("nuxt-link", {
                  staticClass: "submenu-link",
                  attrs: {
                      to: "/" + link.cached_path,
                      itemprop: "url"
                  }
              }, [t._v("\n        " + t._s(link.title) + "\n      ")])], 1)
          }
          )), 0)])
      }
      ), [], !1, null, "265e2246", null).exports)
        , y = r(17)
        , k = r(42)
        , w = r(336)
        , S = r.n(w)
        , x = r(92)
        , $ = r.n(x)
        , M = r(389)
        , O = r(400)
        , I = r(421);
      function E(object, t) {
          var e = Object.keys(object);
          if (Object.getOwnPropertySymbols) {
              var r = Object.getOwnPropertySymbols(object);
              t && (r = r.filter((function(t) {
                  return Object.getOwnPropertyDescriptor(object, t).enumerable
              }
              ))),
              e.push.apply(e, r)
          }
          return e
      }
      function H(t) {
          for (var i = 1; i < arguments.length; i++) {
              var source = null != arguments[i] ? arguments[i] : {};
              i % 2 ? E(Object(source), !0).forEach((function(e) {
                  Object(y.a)(t, e, source[e])
              }
              )) : Object.getOwnPropertyDescriptors ? Object.defineProperties(t, Object.getOwnPropertyDescriptors(source)) : E(Object(source)).forEach((function(e) {
                  Object.defineProperty(t, e, Object.getOwnPropertyDescriptor(source, e))
              }
              ))
          }
          return t
      }
      var L = {
          name: "HeaderCityChange",
          components: {
              IconBase: l.a,
              IconMagnifier: M.a,
              IconClear: O.a,
              IconCaret: I.a
          },
          computed: H(H({}, Object(k.c)(["cityQuery", "cities", "cityPopular", "cityName", "cityStores"])), {}, {
              cityInfo() {
                  return "Ваш город " + this.cityName
              }
          }),
          created() {
              this.getCities("")
          },
          mounted() {
              ({
                  init() {
                      this.initHeaderGeo()
                  },
                  initHeaderGeo() {
                      var t = "is-nr-header-geo-open"
                        , e = "nr-header__geo--not-empty"
                        , r = ".nr-header__geo"
                        , n = ".nr-header__geo-dialog"
                        , o = ".nr-header__geo-input"
                        , c = ".nr-header__geo-clear"
                        , l = ".nr-header__geo-toggler"
                        , html = document.documentElement
                        , h = document.querySelector(r);
                      if (null !== h) {
                          var d = h.querySelector(n)
                            , _ = h.querySelector(o)
                            , v = h.querySelector(c)
                            , m = ()=>{
                              "" !== _.value ? h.classList.add(e) : h.classList.remove(e)
                          }
                          ;
                          ["keydown", "input", "paste"].forEach((t=>{
                              _.addEventListener(t, $()(m, 100))
                          }
                          )),
                          v.addEventListener("click", (e=>{
                              _.value = "",
                              m(),
                              html.classList.remove(t),
                              e.preventDefault()
                          }
                          )),
                          m(),
                          h.addEventListener("click", (e=>{
                              d.contains(e.target) || html.classList.remove(t)
                          }
                          ))
                      }
                      var C = document.querySelector(l);
                      null !== C && C.addEventListener("click", (e=>{
                          html.classList.toggle(t),
                          e.preventDefault()
                      }
                      ))
                  }
              }).init()
          },
          methods: H(H({}, Object(k.b)(["getCities", "setCurrentCity"])), {}, {
              updateCityQuery: S()((function(t) {
                  this.getCities(t.target.value)
              }
              ), 1e3),
              changeCity(t) {
                  document.documentElement.classList.remove("is-nr-header-geo-open"),
                  this.setCurrentCity(t)
              }
          })
      }
        , j = (r(894),
      Object(o.a)(L, (function() {
          var t = this
            , e = t.$createElement
            , r = t._self._c || e;
          return r("li", {
              staticClass: "nr-header__topbar-item nr-header__topbar-item--region"
          }, [r("a", {
              staticClass: "nr-header__topbar-link nr-header__geo-toggler",
              attrs: {
                  title: t.cityInfo,
                  href: "#"
              }
          }, [t._v(t._s(t.cityInfo) + "\n    "), r("div", {
              staticClass: "caret"
          }, [r("IconBase", {
              attrs: {
                  "icon-name": "caret"
              }
          }, [r("IconCaret")], 1)], 1)]), t._v(" "), r("div", {
              staticClass: "nr-header__geo"
          }, [r("div", {
              staticClass: "nr-header__geo-container nr-container"
          }, [r("div", {
              staticClass: "nr-header__geo-dialog"
          }, [r("form", {
              staticClass: "nr-header__geo-form",
              attrs: {
                  action: ""
              }
          }, [r("div", {
              staticClass: "nr-header__geo-input-container"
          }, [r("input", {
              staticClass: "nr-header__geo-input",
              attrs: {
                  type: "text",
                  autofocus: "autofocus",
                  name: "city",
                  size: "30",
                  placeholder: "Введите название города"
              },
              domProps: {
                  value: t.cityQuery
              },
              on: {
                  input: t.updateCityQuery
              }
          }), t._v(" "), r("span", {
              staticClass: "nr-header__geo-icon"
          }, [r("IconBase", {
              attrs: {
                  "icon-name": "magnifier"
              }
          }, [r("IconMagnifier")], 1)], 1), t._v(" "), r("span", {
              staticClass: "nr-header__geo-buttons"
          }, [r("button", {
              staticClass: "nr-header__geo-clear",
              attrs: {
                  type: "button",
                  "aria-label": "Очистить"
              }
          }, [r("IconBase", {
              attrs: {
                  "icon-name": "clear"
              }
          }, [r("IconClear")], 1)], 1)])]), t._v(" "), t.cities ? r("div", {
              staticClass: "nr-header__geo-suggest"
          }, t._l(t.cities, (function(e, n) {
              return r("div", {
                  key: n,
                  staticClass: "nr-header__geo-suggest-item",
                  on: {
                      click: function(r) {
                          return t.changeCity(e.attributes)
                      }
                  }
              }, [t._v("\n              " + t._s(e.attributes.title_with_region) + "\n            ")])
          }
          )), 0) : t._e()])])])])])
      }
      ), [], !1, null, "bfa85f28", null).exports)
        , A = r(1)
        , B = (r(345),
      {
          name: "HeaderSearchResultsItems",
          components: {
              Currency: r(280).a
          },
          props: {
              item: {
                  type: Object,
                  required: !0
              }
          }
      })
        , D = (r(895),
      Object(o.a)(B, (function() {
          var t = this
            , e = t.$createElement
            , r = t._self._c || e;
          return r("div", {
              staticClass: "search-item"
          }, [r("div", {
              staticClass: "search-item-photo"
          }, [r("img", {
              staticClass: "search-item-img",
              attrs: {
                  src: t.item.attributes.image.media.small.url,
                  alt: t.item.attributes.title
              }
          })]), t._v(" "), r("div", {
              staticClass: "search-item-info"
          }, [r("div", {
              staticClass: "search-item-brand"
          }, [t._v("\n      " + t._s(t.item.attributes.manufacturer ? t.item.attributes.manufacturer.title : "") + "\n    ")]), t._v(" "), r("div", {
              staticClass: "search-item-title"
          }, [r("nuxt-link", {
              staticClass: "search-item-link",
              attrs: {
                  to: "/" + t.item.attributes.category_cached_path + "/" + t.item.attributes.sku + "-" + t.item.attributes.slug,
                  title: t.item.attributes.title
              }
          }, [t._v("\n        " + t._s(t.item.attributes.title) + "\n      ")])], 1), t._v(" "), r("div", {
              staticClass: "search-item-price"
          }, [t._v("\n      " + t._s(t._f("priceFormat")(t.item.attributes.price)) + "\n      "), r("Currency")], 1), t._v(" "), r("nuxt-link", {
              staticClass: "search-item-buy",
              attrs: {
                  to: "/" + t.item.attributes.category_cached_path + "/" + t.item.attributes.sku + "-" + t.item.attributes.slug,
                  title: t.item.attributes.title
              }
          }, [t._v("\n      Купить\n    ")])], 1)])
      }
      ), [], !1, null, "7d1efc7c", null).exports)
        , N = {
          name: "HeaderSearchForm",
          components: {
              IconBase: l.a,
              IconMagnifier: M.a,
              IconClear: O.a,
              HeaderSearchResultsItems: D
          },
          data: ()=>({
              suggestCategories: null,
              suggestItems: null,
              suggestQueries: null,
              popupStatus: !1,
              isReady: !1
          }),
          computed: {
              searchPopular() {
                  return this.$store.getters.searchPopular
              },
              searchQuery() {
                  return this.$store.getters["catalog/searchQuery"]
              }
          },
          watch: {
              searchQuery(t) {
                  "" === t && (this.suggestCategories = null,
                  this.suggestItems = null,
                  this.suggestQueries = null)
              },
              "$route.path": {
                  handler: function(path) {
                      "/search" !== path ? this.clearSearchQuery() : this.$store.commit("catalog/SET_SEARCH_QUERY", this.$route.query.query)
                  },
                  deep: !0,
                  immediate: !0
              }
          },
          mounted() {
              var t = this;
              return Object(A.a)((function*() {
                  yield t.$store.dispatch("getSearchPopular"),
                  t.isReady = !0
              }
              ))()
          },
          methods: {
              clearSearchQuery() {
                  this.$store.commit("catalog/SET_SEARCH_QUERY", "")
              },
              inputSearchFocus() {
                  this.$refs.inputSearch.focus()
              },
              handleHide() {
                  this.$emit("hide"),
                  this.popupStatus = !1
              },
              handleShow() {
                  this.$emit("show"),
                  this.popupStatus = !0
              },
              submitSearch(t) {
                  this.$store.commit("catalog/SET_SEARCH_QUERY", t),
                  t.length > 1 && (this.handleHide(),
                  this.debouncedRouterPush(t))
              },
              handleInputSearch(t) {
                  this.$store.commit("catalog/SET_SEARCH_QUERY", t.target.value),
                  this.throttledSearchSuggest()
              },
              debouncedRouterPush: S()((function(t) {
                  this.$router.push("/search?query=" + t).catch((()=>{}
                  ))
              }
              ), 1e3, {
                  leading: !0,
                  trailing: !1
              }),
              throttledSearchSuggest: $()((function() {
                  this.searchQuery.length > 1 && this.$axios.$post("search/suggest", {
                      query: this.searchQuery.trim()
                  }).then((t=>{
                      if (t)
                          try {
                              t.items.data && (this.suggestItems = t.items.data),
                              t.queries.length && (this.suggestQueries = t.queries),
                              t.categories.data.length && (this.suggestCategories = t.categories.data)
                          } catch (t) {}
                  }
                  )).catch((t=>{}
                  ))
              }
              ), 3e3)
          }
      }
        , Q = (r(896),
      Object(o.a)(N, (function() {
          var t = this
            , e = t.$createElement
            , r = t._self._c || e;
          return r("div", {
              staticClass: "nr-header__search"
          }, [r("form", {
              staticClass: "nr-header__search-form",
              on: {
                  submit: function(e) {
                      return e.preventDefault(),
                      t.submitSearch(t.searchQuery)
                  }
              }
          }, [r("div", {
              staticClass: "nr-header__search-input-container"
          }, [r("input", {
              ref: "inputSearch",
              staticClass: "nr-header__search-input",
              attrs: {
                  disabled: !t.isReady,
                  size: "30",
                  type: "text",
                  placeholder: "Поиск"
              },
              domProps: {
                  value: t.searchQuery
              },
              on: {
                  focus: t.handleShow,
                  blur: t.handleHide,
                  input: t.handleInputSearch
              }
          }), t._v(" "), r("span", {
              staticClass: "nr-header__search-icon"
          }, [r("IconBase", {
              attrs: {
                  "icon-name": "magnifier"
              }
          }, [r("IconMagnifier")], 1)], 1), t._v(" "), r("span", {
              staticClass: "nr-header__search-buttons mob",
              class: {
                  isActive: t.searchQuery
              }
          }, [r("button", {
              staticClass: "nr-header__search-clear",
              attrs: {
                  type: "button",
                  "aria-label": "Очистить"
              },
              on: {
                  click: t.clearSearchQuery
              }
          }, [r("IconBase", {
              attrs: {
                  "icon-name": "clear"
              }
          }, [r("IconClear")], 1)], 1)]), t._v(" "), r("span", {
              staticClass: "nr-header__search-buttons search-desc",
              class: {
                  isActive: t.searchQuery
              }
          }, [r("button", {
              staticClass: "nr-header__search-clear",
              attrs: {
                  type: "button",
                  "aria-label": "Очистить"
              },
              on: {
                  click: t.clearSearchQuery
              }
          }, [r("IconBase", {
              attrs: {
                  "icon-name": "clear"
              }
          }, [r("IconClear")], 1)], 1), t._v(" "), r("button", {
              staticClass: "nr-header__search-submit",
              attrs: {
                  title: "Найти",
                  type: "submit"
              }
          }, [t._v("\n          Найти\n        ")])])]), t._v(" "), r("div", {
              staticClass: "nr-header__search-popup",
              class: {
                  isActive: t.popupStatus
              }
          }, [t.suggestItems || t.suggestCategories || t.suggestQueries ? r("div", {
              staticClass: "search-results"
          }, [t.suggestCategories || t.suggestQueries ? r("div", {
              staticClass: "search-results-left"
          }, [t.suggestQueries ? t._l(t.suggestQueries, (function(e, n) {
              return r("div", {
                  key: n,
                  staticClass: "nr-header__search-popup-item",
                  on: {
                      click: function(r) {
                          return r.preventDefault(),
                          t.submitSearch(e)
                      }
                  }
              }, [t._v("\n              " + t._s(e) + "\n            ")])
          }
          )) : t._e(), t._v(" "), t.suggestCategories ? [r("div", {
              staticClass: "nr-header__search-popup-header"
          }, [t._v("\n              Категории\n            ")]), t._v(" "), r("ul", {
              staticClass: "search-results-categories"
          }, t._l(t.suggestCategories, (function(e, n) {
              return r("li", {
                  key: n,
                  staticClass: "search-results-category"
              }, [r("nuxt-link", {
                  staticClass: "search-results-link",
                  attrs: {
                      to: "/" + e.attributes.cached_path,
                      title: e.attributes.title
                  }
              }, [t._v("\n                  " + t._s(e.attributes.title) + "\n                ")])], 1)
          }
          )), 0)] : t._e()], 2) : t._e(), t._v(" "), t.suggestItems ? r("div", {
              staticClass: "search-results-right"
          }, t._l(t.suggestItems, (function(t, e) {
              return r("HeaderSearchResultsItems", {
                  key: e,
                  attrs: {
                      item: t
                  }
              })
          }
          )), 1) : t._e()]) : [r("div", {
              staticClass: "nr-header__search-popup-header"
          }, [t._v("\n          Популярные запросы\n        ")]), t._v(" "), t._l(t.searchPopular, (function(e, n) {
              return r("div", {
                  key: n,
                  staticClass: "nr-header__search-popup-item",
                  on: {
                      click: function(r) {
                          return r.preventDefault(),
                          t.submitSearch(e)
                      }
                  }
              }, [t._v("\n          " + t._s(e) + "\n        ")])
          }
          ))]], 2)]), t._v(" "), r("div", {
              staticClass: "search-overlay",
              on: {
                  click: t.handleHide
              }
          })])
      }
      ), [], !1, null, "342735b4", null).exports)
        , P = r(355)
        , U = Object(o.a)({}, (function() {
          var t = this
            , e = t.$createElement
            , r = t._self._c || e;
          return r("svg", {
              attrs: {
                  width: "24",
                  height: "24",
                  viewBox: "0 0 24 24",
                  fill: "none",
                  xmlns: "http://www.w3.org/2000/svg"
              }
          }, [r("path", {
              attrs: {
                  d: "M19.5555 6.5L20.4412 22H3.55877L4.44449 6.5H19.5555Z",
                  fill: "#111111",
                  stroke: "#111111",
                  "stroke-width": "2"
              }
          }), t._v(" "), r("path", {
              attrs: {
                  d: "M16 10V5C16 2.79086 14.2091 1 12 1V1C9.79086 1 8 2.79086 8 5V10",
                  stroke: "#111111",
                  "stroke-width": "2"
              }
          })])
      }
      ), [], !1, null, null, null).exports
        , F = Object(o.a)({}, (function() {
          var t = this.$createElement
            , e = this._self._c || t;
          return e("svg", {
              attrs: {
                  width: "24",
                  height: "24",
                  viewBox: "0 0 24 24",
                  xmlns: "http://www.w3.org/2000/svg"
              }
          }, [e("path", {
              attrs: {
                  d: "M 7.5,3 C 4.4350952,3 2,5.4084636 2,8.4101562 c 0,1.8354128 0.84186,3.5569628 2.3496094,5.3613278 1.5186521,1.817354 3.6301262,3.669636 6.2499996,5.949219 l 0.002,0.002 L 12,21 l 1.396484,-1.275391 0.0039,-0.0039 c 0.155351,-0.140893 0.308521,-0.279872 0.460937,-0.417969 2.362605,-2.140004 4.311545,-3.896009 5.751953,-5.605468 C 21.139679,11.885558 22,10.201233 22,8.4101562 22,5.4084745 19.564937,3 16.5,3 14.780719,3 13.113207,3.7723739 12,5.0664062 10.886798,3.7723793 9.2192963,3 7.5,3 Z m 0,2 c 1.0951437,0 2.2755769,0.5452076 2.984375,1.3691406 L 12,8.1328125 13.515625,6.3691406 C 14.224418,5.5452131 15.404881,5 16.5,5 18.561863,5 20,6.4490782 20,8.4101562 c 0,1.1566428 -0.540607,2.3655488 -1.916016,3.9980468 -1.299591,1.542341 -3.201858,3.272115 -5.564453,5.412109 -0.14997,0.135882 -0.302904,0.274287 -0.457031,0.414063 l -0.0078,0.0059 -0.05469,0.05078 -0.05273,-0.04687 -0.01758,-0.01758 -0.01758,-0.01562 0,0.002 C 9.297933,15.93818 7.2435535,14.114327 5.8847656,12.488281 4.536895,10.875247 4,9.647064 4,8.4101562 4,6.449089 5.4381848,5 7.5,5 Z"
              }
          })])
      }
      ), [], !1, null, null, null).exports
        , R = r(287)
        , z = r(370)
        , T = {
          name: "TheHeader",
          components: {
              DesktopCategories: c,
              HeaderUserMenu: d,
              HeaderMobileNavMenu: m,
              HeaderCategories: f,
              HeaderCityChange: j,
              HeaderSearchForm: Q,
              IconBase: l.a,
              IconCart: P.a,
              IconCartFull: U,
              IconHeart: F,
              IconMagnifier: M.a,
              Modal: R.a,
              AuthBlock: z.a
          },
          middleware: "auth",
          data: ()=>({
              isShowSearchForm: !1,
              isShowMobileNavMenu: !1,
              isShowDesktopCategories: !1
          }),
          computed: {
              city() {
                  return this.$store.getters.city
              },
              categories() {
                  return this.$store.state.categories.items
              },
              isShowAuthModal() {
                  return this.$store.getters["modal/isShowAuthModal"]
              },
              description() {
                  return this.$store.getters["meta/description"]
              },
              headline() {
                  return this.$store.getters["meta/headline"]
              }
          },
          mounted() {
              this.$store.dispatch("categories/getCategories")
          },
          methods: {
              showSearchForm() {
                  this.isShowSearchForm = !0,
                  this.$nextTick((function() {
                      this.$refs.headerSearchForm.inputSearchFocus()
                  }
                  ))
              },
              hideSearchForm() {
                  this.isShowSearchForm = !1
              },
              handleCloseAuthModal() {
                  this.$store.commit("modal/CLOSE_AUTH_MODAL"),
                  this.isShowMobileNavMenu = !1
              },
              handleOpenAuthModal() {
                  this.$store.commit("modal/SHOW_AUTH_MODAL")
              }
          }
      }
        , W = (r(897),
      Object(o.a)(T, (function() {
          var t = this
            , e = t.$createElement
            , n = t._self._c || e;
          return n("header", {
              staticClass: "nr-header",
              class: {
                  "is-nr-header-search-open": t.isShowSearchForm,
                  "is-nr-header-mobile-nav-open": t.isShowMobileNavMenu || t.isShowDesktopCategories
              },
              attrs: {
                  itemscope: "",
                  itemtype: "https://schema.org/WPHeader"
              }
          }, [n("meta", {
              attrs: {
                  itemprop: "headline",
                  content: t.headline
              }
          }), t._v(" "), n("meta", {
              attrs: {
                  itemprop: "description",
                  content: t.description
              }
          }), t._v(" "), n("meta", {
              attrs: {
                  itemprop: "keywords",
                  content: ""
              }
          }), t._v(" "), n("div", {
              staticClass: "nr-header__overlay",
              class: {
                  isActive: t.isShowSearchForm
              }
          }), t._v(" "), n("div", {
              staticClass: "nr-header__topbar"
          }, [n("div", {
              staticClass: "nr-header__topbar-container nr-container"
          }, [n("div", {
              staticClass: "nr-header__topbar-row"
          }, [n("div", {
              staticClass: "nr-header__topbar-col nr-header__topbar-col--left"
          }, [n("ul", {
              staticClass: "nr-header__topbar-list nr-header__topbar-list--shops"
          }, [n("HeaderCityChange"), t._v(" "), n("li", {
              staticClass: "nr-header__topbar-item"
          }, [n("nuxt-link", {
              staticClass: "nr-header__topbar-link",
              attrs: {
                  to: "/stores/",
                  title: "Адреса магазинов"
              }
          }, [t._v("\n                Адреса магазинов\n              ")])], 1)], 1)]), t._v(" "), n("div", {
              staticClass: "nr-header__topbar-col nr-header__topbar-col--right"
          }, [n("ul", {
              staticClass: "nr-header__topbar-list"
          }, [n("li", {
              staticClass: "nr-header__topbar-item"
          }, [n("nuxt-link", {
              staticClass: "nr-header__topbar-link nr-header__topbar-link--grey",
              attrs: {
                  to: "/delivery/",
                  title: "Доставка и оплата"
              }
          }, [t._v("\n                Доставка и оплата\n              ")])], 1), t._v(" "), n("li", {
              staticClass: "nr-header__topbar-item",
              attrs: {
                  itemscope: "",
                  itemtype: "http://schema.org/Organization"
              }
          }, [n("meta", {
              attrs: {
                  content: "Книжный интернет-магазин «Республика»",
                  itemprop: "name"
              }
          }), t._v(" "), n("div", {
              attrs: {
                  itemprop: "address",
                  itemscope: "",
                  itemtype: "http://schema.org/PostalAddress"
              }
          }, [n("meta", {
              attrs: {
                  content: "Каспийская ул, дом 22",
                  itemprop: "streetAddress"
              }
          }), t._v(" "), n("meta", {
              attrs: {
                  content: "115304",
                  itemprop: "postalCode"
              }
          }), t._v(" "), n("meta", {
              attrs: {
                  content: "г. Москва",
                  itemprop: "addressLocality"
              }
          }), t._v(" "), n("meta", {
              attrs: {
                  content: "+7(499)444-33-67",
                  itemprop: "telephone"
              }
          }), t._v(" "), n("meta", {
              attrs: {
                  content: "store@respublica-pro.ru",
                  itemprop: "email"
              }
          }), t._v(" "), n("a", {
              staticClass: "nr-header__topbar-link nr-header__topbar-link--grey",
              attrs: {
                  href: "tel:" + t.$store.state.cityPhone
              }
          }, [t._v(t._s(t.$store.state.cityPhone))])])])])])])])]), t._v(" "), n("div", {
              staticClass: "nr-header__main"
          }, [n("div", {
              staticClass: "nr-header__main-container nr-container"
          }, [n("div", {
              staticClass: "nr-header__main-row"
          }, [n("div", {
              staticClass: "nr-header__main-col nr-header__main-col--left"
          }, [n("button", {
              staticClass: "nr-header__burger-mobile",
              attrs: {
                  type: "button"
              },
              on: {
                  click: function(e) {
                      t.isShowMobileNavMenu = !t.isShowMobileNavMenu
                  }
              }
          }, [t._m(0), t._v(" "), n("span", {
              staticClass: "nr-header__burger-text"
          }, [t._v("\n              Меню\n            ")])]), t._v(" "), n("div", {
              staticClass: "nr-header__logo"
          }, [n("nuxt-link", {
              attrs: {
                  to: "/",
                  title: "Книжный интернет-магазин «Республика»"
              }
          }, [n("img", {
              attrs: {
                  src: r(382),
                  alt: "Книжный интернет-магазин «Республика»",
                  sizes: "(max-width: 976px) 190px, (min-width: 976px) 263px"
              }
          })])], 1), t._v(" "), n("button", {
              staticClass: "nr-header__burger-desktop",
              attrs: {
                  type: "button"
              },
              on: {
                  click: function(e) {
                      t.isShowDesktopCategories = !t.isShowDesktopCategories
                  }
              }
          }, [t._m(1), t._v(" "), n("span", {
              staticClass: "nr-header__burger-desktop-text"
          }, [t._v("\n              Каталог\n            ")])])]), t._v(" "), n("div", {
              staticClass: "nr-header__main-col nr-header__main-col--right"
          }, [n("HeaderSearchForm", {
              ref: "headerSearchForm",
              on: {
                  show: t.showSearchForm,
                  hide: t.hideSearchForm
              }
          }), t._v(" "), n("div", {
              staticClass: "nr-header__user-nav"
          }, [n("div", {
              staticClass: "\n                nr-header__user-nav-item nr-header__user-nav-item--search\n              "
          }, [n("button", {
              staticClass: "\n                  nr-header__user-nav-link\n                  nr-header__user-nav-link--button\n                  nr-header__user-nav-link--search\n                ",
              attrs: {
                  type: "button",
                  "aria-label": "Поиск"
              },
              on: {
                  click: t.showSearchForm
              }
          }, [n("IconBase", {
              staticClass: "header-icon",
              attrs: {
                  "icon-name": "magnifier"
              }
          }, [n("IconMagnifier")], 1)], 1)]), t._v(" "), n("HeaderUserMenu", {
              on: {
                  showAuth: t.handleOpenAuthModal
              }
          }), t._v(" "), n("div", {
              staticClass: "nr-header__user-nav-item nr-header__user-nav-item--wish"
          }, [t.$store.getters.currentUser ? n("nuxt-link", {
              staticClass: "nr-header__user-nav-link",
              attrs: {
                  to: "/my/wishlist",
                  title: "Избранное"
              }
          }, [n("IconBase", {
              staticClass: "header-icon",
              attrs: {
                  "icon-name": "heart"
              }
          }, [n("IconHeart")], 1)], 1) : n("a", {
              staticClass: "nr-header__user-nav-link",
              attrs: {
                  href: "#",
                  title: "Избранное"
              },
              on: {
                  click: function(e) {
                      return e.preventDefault(),
                      t.handleOpenAuthModal.apply(null, arguments)
                  }
              }
          }, [n("IconBase", {
              staticClass: "header-icon",
              attrs: {
                  "icon-name": "heart"
              }
          }, [n("IconHeart")], 1)], 1)], 1), t._v(" "), n("div", {
              staticClass: "nr-header__user-nav-item"
          }, [n("nuxt-link", {
              staticClass: "nr-header__user-nav-link",
              attrs: {
                  to: "/cart",
                  title: "Корзина"
              }
          }, [n("IconBase", {
              staticClass: "header-icon"
          }, [0 === t.$store.getters.itemsCount ? n("IconCart") : n("IconCartFull")], 1), t._v(" "), n("span", {
              staticClass: "nr-header__badge nr-header__badge--blue"
          }, [t._v("\n                  " + t._s(t.$store.getters.itemsCount) + "\n                ")])], 1)], 1)], 1)], 1)]), t._v(" "), n("HeaderCategories", {
              staticClass: "nav-desktop"
          })], 1)]), t._v(" "), t.isShowMobileNavMenu ? n("HeaderMobileNavMenu", {
              on: {
                  hide: function(e) {
                      t.isShowMobileNavMenu = !1
                  },
                  showAuth: t.handleOpenAuthModal
              }
          }) : t._e(), t._v(" "), n("transition", {
              attrs: {
                  name: "fade-nav",
                  mode: "out-in"
              }
          }, [t.isShowDesktopCategories ? n("DesktopCategories", {
              on: {
                  hide: function(e) {
                      t.isShowDesktopCategories = !1
                  }
              }
          }) : t._e()], 1), t._v(" "), n("portal", {
              attrs: {
                  to: "popups"
              }
          }, [n("transition", {
              attrs: {
                  name: "fade"
              }
          }, [t.isShowAuthModal ? n("Modal", {
              attrs: {
                  "max-width": "480px",
                  "max-height": "580px",
                  "has-close-button": ""
              },
              on: {
                  close: t.handleCloseAuthModal
              }
          }, [n("AuthBlock", {
              on: {
                  closeAuth: t.handleCloseAuthModal
              }
          })], 1) : t._e()], 1)], 1)], 1)
      }
      ), [function() {
          var t = this.$createElement
            , e = this._self._c || t;
          return e("span", {
              staticClass: "nr-header__burger-icon"
          }, [e("span", {
              staticClass: "nr-header__burger-icon-line"
          })])
      }
      , function() {
          var t = this.$createElement
            , e = this._self._c || t;
          return e("span", {
              staticClass: "nr-header__burger-icon"
          }, [e("span", {
              staticClass: "nr-header__burger-icon-line"
          })])
      }
      ], !1, null, null, null));
      e.default = W.exports
  }
}]);
