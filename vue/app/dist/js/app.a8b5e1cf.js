(function(e){function t(t){for(var o,s,c=t[0],i=t[1],l=t[2],p=0,f=[];p<c.length;p++)s=c[p],Object.prototype.hasOwnProperty.call(a,s)&&a[s]&&f.push(a[s][0]),a[s]=0;for(o in i)Object.prototype.hasOwnProperty.call(i,o)&&(e[o]=i[o]);u&&u(t);while(f.length)f.shift()();return r.push.apply(r,l||[]),n()}function n(){for(var e,t=0;t<r.length;t++){for(var n=r[t],o=!0,c=1;c<n.length;c++){var i=n[c];0!==a[i]&&(o=!1)}o&&(r.splice(t--,1),e=s(s.s=n[0]))}return e}var o={},a={app:0},r=[];function s(t){if(o[t])return o[t].exports;var n=o[t]={i:t,l:!1,exports:{}};return e[t].call(n.exports,n,n.exports,s),n.l=!0,n.exports}s.m=e,s.c=o,s.d=function(e,t,n){s.o(e,t)||Object.defineProperty(e,t,{enumerable:!0,get:n})},s.r=function(e){"undefined"!==typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},s.t=function(e,t){if(1&t&&(e=s(e)),8&t)return e;if(4&t&&"object"===typeof e&&e&&e.__esModule)return e;var n=Object.create(null);if(s.r(n),Object.defineProperty(n,"default",{enumerable:!0,value:e}),2&t&&"string"!=typeof e)for(var o in e)s.d(n,o,function(t){return e[t]}.bind(null,o));return n},s.n=function(e){var t=e&&e.__esModule?function(){return e["default"]}:function(){return e};return s.d(t,"a",t),t},s.o=function(e,t){return Object.prototype.hasOwnProperty.call(e,t)},s.p="/";var c=window["webpackJsonp"]=window["webpackJsonp"]||[],i=c.push.bind(c);c.push=t,c=c.slice();for(var l=0;l<c.length;l++)t(c[l]);var u=i;r.push([0,"chunk-vendors"]),n()})({0:function(e,t,n){e.exports=n("56d7")},"034f":function(e,t,n){"use strict";n("85ec")},"1d1c":function(e,t,n){"use strict";n("2656")},2656:function(e,t,n){},"56d7":function(e,t,n){"use strict";n.r(t);n("e260"),n("e6cf"),n("cca6"),n("a79d");var o=n("2b0e"),a=function(){var e=this,t=e.$createElement,o=e._self._c||t;return o("div",{attrs:{id:"app"}},[o("img",{attrs:{alt:"Vue logo",src:n("cf05")}}),o("HelloWorld",{attrs:{msg:"Welcome to HU"}}),o("el-upload",{staticClass:"upload-demo",attrs:{action:"http://localhost/store/api/newproducts/","on-preview":e.handlePreview,"on-remove":e.handleRemove,headers:{Authorization:e.accessToken},data:{name:"lionhu"},"file-list":e.fileList,"list-type":"picture"}},[o("el-button",{attrs:{size:"small",type:"primary"}},[e._v("点击上传")]),o("div",{staticClass:"el-upload__tip",attrs:{slot:"tip"},slot:"tip"},[e._v("只能上传jpg/png文件，且不超过500kb")])],1)],1)},r=[],s=(n("4160"),n("b0c0"),n("159b"),n("d3b7"),n("bc3a")),c=n.n(s),i=sessionStorage.getItem("accessToken");function l(e,t){return new Promise((function(n){var o=c.a.post("".concat(e),t,{headers:{"content-type":"multipart/form-data"}}).then((function(e){return{payload:e}})).catch((function(e){return{error:e}}));console.log(o),n(o)}))}function u(e,t){return new Promise((function(n){var o=c.a.get("".concat(e),t,{headers:{"content-type":"application/json",Authorization:i||""}}).then((function(e){return{payload:e}})).catch((function(e){return{error:e}}));n(o)}))}function p(e,t){return new Promise((function(n){var o=c.a.post("".concat(e),t,{headers:{"content-type":"application/json",Authorization:i||""}}).then((function(e){return{payload:e}})).catch((function(e){return{error:e}}));n(o)}))}c.a.defaults.baseURL="http://localhost:8000",c.a.defaults.xsrfCookieName="csrftoken",c.a.defaults.xsrfHeaderName="X-CSRFToken",c.a.defaults.headers.common.Authorization=i;var f=n("5c96"),d=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",{staticClass:"hello"},[n("h1",[e._v(e._s(e.msg))]),n("h3",{staticClass:"lionhu"},[e._v("by Lionhu")])])},h=[],m={name:"HelloWorld",props:{msg:String},data:function(){return{}},components:{},methods:{}},g=m,v=(n("1d1c"),n("2877")),b=Object(v["a"])(g,d,h,!1,null,"21e70ae4",null),y=b.exports,w={name:"App",components:{HelloWorld:y,"el-upload":f["Upload"],"el-button":f["Button"]},computed:{accessToken:function(){return sessionStorage.getItem("accessToken")?sessionStorage.getItem("accessToken"):""}},data:function(){return{fileList:[],uploadimage:null,headers:{"content-type":"multipart/form-data",Authorization:this.access_token}}},methods:{handleRemove:function(e,t){console.log(e,t)},handlePreview:function(e){console.log(e)},submitUpload:function(){console.log(this.$refs.upload),this.$refs.upload.submit()},handleAvatarSuccess:function(e,t){console.log(e),console.log(t)},beforeAvatarUpload:function(e){var t="image/jpeg"===e.type,n=e.size/1024/1024<2;return t||this.$message.error("上传头像图片只能是 JPG 格式!"),n||this.$message.error("上传头像图片大小不能超过 2MB!"),t&&n},onFileChange:function(e){var t=e.target.files||e.dataTransfer.files;this.img_name=t[0];var n=new FormData;n.append("name","huhaiguang"),n.append("file",this.img_name),l("/store/api/newproducts/",n).then((function(e){console.log(e)}))}},mounted:function(){var e=this,t=new FormData;t.append("email","huhaiguang@me.com"),t.append("username","admin"),t.append("password","lionhu"),p("/apiauth/login/",t).then((function(e){console.log(e.payload),200===e.payload.status&&(sessionStorage.removeItem("accessToken"),sessionStorage.setItem("accessToken","Bearer ".concat(e.payload.data.tokens.access)),console.log(sessionStorage.getItem("accessToken")))})),u("/store/api/newproducts/").then((function(t){console.log(t.payload.data);var n=t.payload.data,o=[];n.forEach((function(e){o.push({name:e.name,url:"http://localhost/"+e.file})})),console.log(o),e.fileList=o}))}},k=w,_=(n("034f"),Object(v["a"])(k,a,r,!1,null,null,null)),j=_.exports;n("0fae");n("c6e4"),o["default"].config.productionTip=!1,new o["default"]({render:function(e){return e(j)}}).$mount("#app")},"85ec":function(e,t,n){},c6e4:function(e,t,n){"use strict";n.r(t),n.d(t,"fileUpload",(function(){return r}));n("d3b7");var o=n("bc3a"),a=n.n(o);function r(e,t){return new Promise((function(n){var o=a.a.post("".concat(e,"/"),t,{headers:{"content-type":"multipart/form-data"}}).then((function(e){return{payload:e}})).catch((function(e){return{error:e}}));n(o)}))}a.a.defaults.baseURL="http://localhost:8000",a.a.defaults.xsrfCookieName="csrftoken",a.a.defaults.xsrfHeaderName="X-CSRFToken"},cf05:function(e,t,n){e.exports=n.p+"img/logo.82b9c7a5.png"}});
//# sourceMappingURL=app.a8b5e1cf.js.map