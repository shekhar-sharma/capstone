(function(e){function t(t){for(var a,i,o=t[0],c=t[1],l=t[2],u=0,f=[];u<o.length;u++)i=o[u],r[i]&&f.push(r[i][0]),r[i]=0;for(a in c)Object.prototype.hasOwnProperty.call(c,a)&&(e[a]=c[a]);d&&d(t);while(f.length)f.shift()();return n.push.apply(n,l||[]),s()}function s(){for(var e,t=0;t<n.length;t++){for(var s=n[t],a=!0,o=1;o<s.length;o++){var c=s[o];0!==r[c]&&(a=!1)}a&&(n.splice(t--,1),e=i(i.s=s[0]))}return e}var a={},r={ngrams:0},n=[];function i(t){if(a[t])return a[t].exports;var s=a[t]={i:t,l:!1,exports:{}};return e[t].call(s.exports,s,s.exports,i),s.l=!0,s.exports}i.m=e,i.c=a,i.d=function(e,t,s){i.o(e,t)||Object.defineProperty(e,t,{enumerable:!0,get:s})},i.r=function(e){"undefined"!==typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},i.t=function(e,t){if(1&t&&(e=i(e)),8&t)return e;if(4&t&&"object"===typeof e&&e&&e.__esModule)return e;var s=Object.create(null);if(i.r(s),Object.defineProperty(s,"default",{enumerable:!0,value:e}),2&t&&"string"!=typeof e)for(var a in e)i.d(s,a,function(t){return e[t]}.bind(null,a));return s},i.n=function(e){var t=e&&e.__esModule?function(){return e["default"]}:function(){return e};return i.d(t,"a",t),t},i.o=function(e,t){return Object.prototype.hasOwnProperty.call(e,t)},i.p="/static/dist/";var o=window["webpackJsonp"]=window["webpackJsonp"]||[],c=o.push.bind(o);o.push=t,o=o.slice();for(var l=0;l<o.length;l++)t(o[l]);var d=c;n.push([5,"chunk-vendors"]),s()})({4678:function(e,t,s){var a={"./af":"2bfb","./af.js":"2bfb","./ar":"8e73","./ar-dz":"a356","./ar-dz.js":"a356","./ar-kw":"423e","./ar-kw.js":"423e","./ar-ly":"1cfd","./ar-ly.js":"1cfd","./ar-ma":"0a84","./ar-ma.js":"0a84","./ar-sa":"8230","./ar-sa.js":"8230","./ar-tn":"6d83","./ar-tn.js":"6d83","./ar.js":"8e73","./az":"485c","./az.js":"485c","./be":"1fc1","./be.js":"1fc1","./bg":"84aa","./bg.js":"84aa","./bm":"a7fa","./bm.js":"a7fa","./bn":"9043","./bn.js":"9043","./bo":"d26a","./bo.js":"d26a","./br":"6887","./br.js":"6887","./bs":"2554","./bs.js":"2554","./ca":"d716","./ca.js":"d716","./cs":"3c0d","./cs.js":"3c0d","./cv":"03ec","./cv.js":"03ec","./cy":"9797","./cy.js":"9797","./da":"0f14","./da.js":"0f14","./de":"b469","./de-at":"b3eb","./de-at.js":"b3eb","./de-ch":"bb71","./de-ch.js":"bb71","./de.js":"b469","./dv":"598a","./dv.js":"598a","./el":"8d47","./el.js":"8d47","./en-SG":"cdab","./en-SG.js":"cdab","./en-au":"0e6b","./en-au.js":"0e6b","./en-ca":"3886","./en-ca.js":"3886","./en-gb":"39a6","./en-gb.js":"39a6","./en-ie":"e1d3","./en-ie.js":"e1d3","./en-il":"7333","./en-il.js":"7333","./en-nz":"6f50","./en-nz.js":"6f50","./eo":"65db","./eo.js":"65db","./es":"898b","./es-do":"0a3c","./es-do.js":"0a3c","./es-us":"55c9","./es-us.js":"55c9","./es.js":"898b","./et":"ec18","./et.js":"ec18","./eu":"0ff2","./eu.js":"0ff2","./fa":"8df4","./fa.js":"8df4","./fi":"81e9","./fi.js":"81e9","./fo":"0721","./fo.js":"0721","./fr":"9f26","./fr-ca":"d9f8","./fr-ca.js":"d9f8","./fr-ch":"0e49","./fr-ch.js":"0e49","./fr.js":"9f26","./fy":"7118","./fy.js":"7118","./ga":"5120","./ga.js":"5120","./gd":"f6b4","./gd.js":"f6b4","./gl":"8840","./gl.js":"8840","./gom-latn":"0caa","./gom-latn.js":"0caa","./gu":"e0c5","./gu.js":"e0c5","./he":"c7aa","./he.js":"c7aa","./hi":"dc4d","./hi.js":"dc4d","./hr":"4ba9","./hr.js":"4ba9","./hu":"5b14","./hu.js":"5b14","./hy-am":"d6b6","./hy-am.js":"d6b6","./id":"5038","./id.js":"5038","./is":"0558","./is.js":"0558","./it":"6e98","./it-ch":"6f12","./it-ch.js":"6f12","./it.js":"6e98","./ja":"079e","./ja.js":"079e","./jv":"b540","./jv.js":"b540","./ka":"201b","./ka.js":"201b","./kk":"6d79","./kk.js":"6d79","./km":"e81d","./km.js":"e81d","./kn":"3e92","./kn.js":"3e92","./ko":"22f8","./ko.js":"22f8","./ku":"2421","./ku.js":"2421","./ky":"9609","./ky.js":"9609","./lb":"440c","./lb.js":"440c","./lo":"b29d","./lo.js":"b29d","./lt":"26f9","./lt.js":"26f9","./lv":"b97c","./lv.js":"b97c","./me":"293c","./me.js":"293c","./mi":"688b","./mi.js":"688b","./mk":"6909","./mk.js":"6909","./ml":"02fb","./ml.js":"02fb","./mn":"958b","./mn.js":"958b","./mr":"39bd","./mr.js":"39bd","./ms":"ebe4","./ms-my":"6403","./ms-my.js":"6403","./ms.js":"ebe4","./mt":"1b45","./mt.js":"1b45","./my":"8689","./my.js":"8689","./nb":"6ce3","./nb.js":"6ce3","./ne":"3a39","./ne.js":"3a39","./nl":"facd","./nl-be":"db29","./nl-be.js":"db29","./nl.js":"facd","./nn":"b84c","./nn.js":"b84c","./pa-in":"f3ff","./pa-in.js":"f3ff","./pl":"8d57","./pl.js":"8d57","./pt":"f260","./pt-br":"d2d4","./pt-br.js":"d2d4","./pt.js":"f260","./ro":"972c","./ro.js":"972c","./ru":"957c","./ru.js":"957c","./sd":"6784","./sd.js":"6784","./se":"ffff","./se.js":"ffff","./si":"eda5","./si.js":"eda5","./sk":"7be6","./sk.js":"7be6","./sl":"8155","./sl.js":"8155","./sq":"c8f3","./sq.js":"c8f3","./sr":"cf1e","./sr-cyrl":"13e9","./sr-cyrl.js":"13e9","./sr.js":"cf1e","./ss":"52bd","./ss.js":"52bd","./sv":"5fbd","./sv.js":"5fbd","./sw":"74dc","./sw.js":"74dc","./ta":"3de5","./ta.js":"3de5","./te":"5cbb","./te.js":"5cbb","./tet":"576c","./tet.js":"576c","./tg":"3b1b","./tg.js":"3b1b","./th":"10e8","./th.js":"10e8","./tl-ph":"0f38","./tl-ph.js":"0f38","./tlh":"cf75","./tlh.js":"cf75","./tr":"0e81","./tr.js":"0e81","./tzl":"cf51","./tzl.js":"cf51","./tzm":"c109","./tzm-latn":"b53d","./tzm-latn.js":"b53d","./tzm.js":"c109","./ug-cn":"6117","./ug-cn.js":"6117","./uk":"ada2","./uk.js":"ada2","./ur":"5294","./ur.js":"5294","./uz":"2e8c","./uz-latn":"010e","./uz-latn.js":"010e","./uz.js":"2e8c","./vi":"2921","./vi.js":"2921","./x-pseudo":"fd7e","./x-pseudo.js":"fd7e","./yo":"7f33","./yo.js":"7f33","./zh-cn":"5c3a","./zh-cn.js":"5c3a","./zh-hk":"49ab","./zh-hk.js":"49ab","./zh-tw":"90ea","./zh-tw.js":"90ea"};function r(e){var t=n(e);return s(t)}function n(e){var t=a[e];if(!(t+1)){var s=new Error("Cannot find module '"+e+"'");throw s.code="MODULE_NOT_FOUND",s}return t}r.keys=function(){return Object.keys(a)},r.resolve=n,e.exports=r,r.id="4678"},5:function(e,t,s){e.exports=s("b9d6")},b9d6:function(e,t,s){"use strict";s.r(t);var a,r,n=s("a026"),i=function(){var e=this,t=e.$createElement,s=e._self._c||t;return s("div",[e._m(0),s("div",{staticClass:"form-group"},[s("div",{staticClass:"row"},[s("input",{directives:[{name:"model",rawName:"v-model.trim",value:e.textToGraph,expression:"textToGraph",modifiers:{trim:!0}}],staticClass:"col-lg-12 text-to-graph",attrs:{placeholder:"Your text here"},domProps:{value:e.textToGraph},on:{input:function(t){t.target.composing||(e.textToGraph=t.target.value.trim())},blur:function(t){e.$forceUpdate()}}}),s("div",{staticClass:"col-lg-12 description small"},[e._v("Separate entries using commas")])]),s("div",{staticClass:"row"},[s("div",{staticClass:"col-lg-6 form-group-elements"},[s("label",{attrs:{for:"min-year"}},[e._v("From")]),s("input",{directives:[{name:"model",rawName:"v-model.number",value:e.minYear,expression:"minYear",modifiers:{number:!0}}],attrs:{id:"min-year",type:"number",min:"1640",max:"2018"},domProps:{value:e.minYear},on:{input:function(t){t.target.composing||(e.minYear=e._n(t.target.value))},blur:function(t){e.$forceUpdate()}}}),e._v("\n         \n        "),s("label",{attrs:{for:"max-year"}},[e._v("To")]),s("input",{directives:[{name:"model",rawName:"v-model.number",value:e.maxYear,expression:"maxYear",modifiers:{number:!0}}],attrs:{id:"max-year",type:"number",min:"1640",max:"2018"},domProps:{value:e.maxYear},on:{input:function(t){t.target.composing||(e.maxYear=e._n(t.target.value))},blur:function(t){e.$forceUpdate()}}})]),s("div",{staticClass:"col-lg-4 text-right"},[s("input",{staticClass:"dropdown-toggle btn-secondary",attrs:{type:"button",id:"jurisdictions",value:"Jurisdictions","data-toggle":"dropdown","aria-haspopup":"true","aria-expanded":"false"}}),s("div",{staticClass:"dropdown dropdown-menu",attrs:{"aria-labelledby":"jurisdictions"}},e._l(e.jurisdictions,function(t){return s("button",{key:t[0],staticClass:"dropdown-item",class:{active:e.selectedJurs.indexOf(t)>-1},attrs:{type:"button"},on:{click:function(s){e.toggleJur(t)}}},[e._v("\n            "+e._s(t[1])+"\n          ")])}))]),s("div",{staticClass:"col-lg-2 text-right"},[s("button",{staticClass:"btn-create btn-primary",on:{click:e.createGraph}},[e._v("\n          Graph\n        ")])])]),e.errors.length?s("div",{staticClass:"row"},[s("div",{staticClass:"small alert-danger"},[s("span",[e._v(e._s(e.errors))])])]):e._e(),s("div",{staticClass:"row"},[s("div",{staticClass:"selected-jurs"},[e.selectedJurs.length?s("span",{staticClass:"small"},[e._v("Selected:")]):e._e(),e._l(e.selectedJurs,function(t){return s("span",{key:t[0],staticClass:"small selected-jur",on:{click:function(s){e.toggleJur(t)}}},[e._v("\n          "+e._s(t[1])+"\n        ")])})],2)]),s("br")]),s("div",{staticClass:"graph"},[s("div",{staticClass:"container graph-container"},[s("line-example",{attrs:{chartData:e.chartData}})],1)])])},o=[function(){var e=this,t=e.$createElement,s=e._self._c||t;return s("div",{staticClass:"page-title"},[s("h1",[e._v("Ngrams")])])}],c=(s("6b54"),s("28a5"),s("6c7b"),s("c5f6"),s("1fca")),l=c["b"].reactiveProp,d={extends:c["a"],props:["chartData"],mixins:[l],data:function(){return{options:{responsive:!0,maintainAspectRatio:!1,legend:{labels:{boxWidth:20}},scales:{yAxes:[{gridLines:{color:"rgba(0, 0, 0, 0)"},ticks:{beginAtZero:!0}}],xAxes:[{gridLines:{color:"rgba(0, 0, 0, 0)"}}]}}}},mounted:function(){this.renderChart(this.chartData,this.options)}},u=d,f=s("2877"),b=Object(f["a"])(u,a,r,!1,null,null,null),m=b.exports,j=s("bc3a"),p=s.n(j),h={name:"Main",components:{"line-example":m},beforeMount:function(){this.jurisdictions=snippets.jurisdictions},data:function(){return{chartData:null,textToGraph:"the court, court",minYear:1800,maxYear:2e3,minPossible:1640,maxPossible:2018,jurisdictions:{},selectedJurs:[],colors:["#0276FF","#E878FF","#EDA633","#FF654D","#6350FD"],errors:""}},methods:{isValidNumber:function(){return this.minYear<=this.maxYear&&this.minYear>=this.minPossible&&this.minYear<=this.maxPossible&&this.maxYear>=this.minPossible&&this.maxYear<=this.maxPossible},isValidText:function(){return this.textToGraph.length>0},range:function(e,t){var s=arguments.length>2&&void 0!==arguments[2]?arguments[2]:1;return e=Number(e),t=Number(t),Array(Math.ceil((t-e)/s)).fill(e).map(function(e,t){return e+t*s})},getSelectedJurs:function(){return this.selectedJurs.map(function(e){return e[0]})},getTerms:function(e){var t=e.split(",");return t.map(function(e){return e.trim()})},createGraph:function(){var e=this;if(this.isValidNumber())if(this.isValidText()){var t=this.getTerms(this.textToGraph),s=this.range(this.minYear,this.maxYear);this.chartData={labels:s,datasets:[]};var a=this.getSelectedJurs();a.splice(0,0,"");var r=a.join("&jurisdiction="),n=0,i=function(a){var i=e,o=t[a],c="http://api.case.test:8000/v1/ngrams/?q="+o+r;p.a.get(c).then(function(t){var a=t.data.results[o],r=[];for(var c in a){var l=a[c];for(var d in s){var u=s[d];u>=e.minYear&&u<=e.maxYear&&(r[d]?l[u]&&(r[d]=r[d]+l[u][0]):l[u]?r[d]=l[u][0]:r[d]=0)}}var f=i.chartData.datasets,b="";b=e.colors.length-1>n?e.colors[n]:"#"+(16777215*Math.random()<<0).toString(16),f.push({label:o,borderColor:b,backgroundColor:"rgba(0, 0, 0, 0)",borderWidth:2,data:r}),i.chartData={labels:s,datasets:f},n+=1})};for(var o in t)i(o)}else this.errors="Please enter text";else this.errors="Please choose valid years. Years must be between "+this.minPossible+" and "+this.maxPossible+"."},getRandomInt:function(){return Math.floor(46*Math.random())+5},toggleJur:function(e){this.selectedJurs.indexOf(e)>-1?this.selectedJurs.splice(this.selectedJurs.indexOf(e),1):this.selectedJurs.push(e)}},mounted:function(){this.createGraph()}},v=h,g=Object(f["a"])(v,i,o,!1,null,null,null),x=g.exports;n["a"].config.devtools=!0,n["a"].config.productionTip=!1,new n["a"]({el:"#app",components:{Main:x},template:"<Main/>"})}});
//# sourceMappingURL=ngrams.js.map