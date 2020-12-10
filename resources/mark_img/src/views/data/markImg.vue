<template>
  <div class="container">
    <div class="img_box unselect" ondragstart="return false">
      <!-- <img id="img" src="@/assets/img/timg (3).jpg" alt="" ondragstart="return false" class="unselect"> -->
      <!-- <img
        id="img"
        src="@/assets/img/timg (1).jpg"
        alt=""
        ondragstart="return false"
        class="unselect"
      /> -->
      <!-- <img id="img" src="@/assets/img/timg (2).jpg" alt="" ondragstart="return false" class="unselect"> -->
      <img id="img" src="@/assets/img/美女.jpg" alt="" ondragstart="return false" class="unselect" />
      <!-- <img id="img" src="@/assets/img/white.jpg" alt="" ondragstart="return false" class="unselect"> -->
    </div>
    <!-- 添加标签 -->
    <div class="add_label">
      <Button type="success" size="small" @click="addLabel">新增标签</Button>
      <ul class="add">
        <li class="add_li" v-for="(item, idx) in labelList" :key="idx">
          <Input v-if="isEdit" type="text" placeholder="请输入标签名称" size="small" style="width: 150px" :value="item" @input="inputAddLabel(idx, $event)"></Input>
          <span v-if="!isEdit">{{ item }}</span>
          <img src="@/assets/img/delete_red.png" alt="" class="delete delete_label" @click="delLabel(idx)" />
        </li>
      </ul>
    </div>
    <!-- 选择标签 -->
    <div class="choose_label">
      <ul>
        <li class="cho_li" v-for="(item, idx) in divList" :key="idx">
          <Select :class="[item.id, 'select']" v-model="item.label" size="small" style="width: 150px" @on-change="selectLabel(item)" @on-open-change="openSelect(item, $event)">
            <Option v-for="(label, i) in myLabelList" :value="label" :key="i">{{
              label
            }}</Option>
          </Select>
          <img src="@/assets/img/delete_red.png" alt="" class="delete delete_div" @click="delDiv(item.id)" />
        </li>
      </ul>
      <Button type="success" size="small" @click="submit" v-if="divList.length" style="width: 150px; margin-top: 20px">提交</Button>
    </div>

    <!-- 图片列表 -->
    <img-list @chooseImg="chooseImg"></img-list>
  </div>
</template>
<script>

import ImgList from '@/components/ImgList.vue'
export default {
  name: "MarkImg",
  components: {
    ImgList
  },
  computed: {
    myLabelList () {
      return this.labelList.filter((item) => item);
    },
  },
  // mounted () {
  //   this.initPage()
  // },
  data () {
    return {
      // labelList: [
      //   'eyes',
      //   'ears',
      //   'mouth',
      //   'nose'
      // ],
      labelList: [],
      // divList: [],
      divList: [
        // {
        //   h: 59,
        //   id: "47558337402343754125000305175781",
        //   label: "eyes",
        //   w: 112,
        //   x: 475.5833740234375,
        //   y: 412.5000305175781,
        // },

        // {
        //   h: 54,
        //   id: "878629",
        //   label: "mouth",
        //   w: 137,
        //   x: 400.5999755859375,
        //   y: 559.5,
        // },

        {
          h: 0.03202846975088968,
          id: "833434",
          label: "mouth",
          w: 0.13345195729537365,
          x: 0.4884341637010676,
          y: 0.4592600830367734
        },
      ],
      isEdit: true,
    };
  },
  methods: {
    chooseImg(src) {
      $('#img').attr('src', src)
      setTimeout(() => {
        $('.box').remove()
        this.divList = []
        this.initPage()
      }, 50);
    },
    initPage () {
      var ratio;
      var img_url = document.getElementById("img").src;
      var img = new Image();
      img.src = img_url;
      img.onload = function () {
        ratio = img.width / img.height;
      };

      this.labelList = this.divList.map((item) => item.label);

      var _this = this;

      setTimeout(() => {
        // 新增标签相关
        var addBtn = $("#addBtn");
        var editBtn = $("#editBtn");
        var confirmBtn = $("#confirmBtn");

        // 给截取div选择标签相关

        // 图片标注相关
        var container = $(".container");
        var imgBox = $(".img_box");
        var boxWidth = imgBox.width();
        var boxHeight = imgBox.height();
        var img = $("#img");

        if(ratio > 1) {
          // img.css('width', '100%')
          // img.css('height', img.width() / ratio)
          img.width("100%");
          img.height(img.width() / ratio);

          if(img.height() > boxHeight) {
            img.height(boxHeight);
            img.width(img.height() * ratio);
          }
        } else {
          // img.css('height', '100%')
          // img.css('width', img.height() * ratio)
          img.height("100%");
          img.width(img.height() * ratio);

          if(img.width() > boxWidth) {
            img.width("100%");
            img.height(img.width() / ratio);
          }
        }
        // img.css({ 'position': 'absolute', 'top': '50%', 'left': '50%', 'transform': 'translate(-50%, -50%)' })

        var height = img.height();
        // document.getElementById('img').style.width = ratio * height
        var width = img.width();
        var iTop, iLeft;
        // iTop = img.offset().top - img.position().top
        // iLeft = img.offset().left - img.position().left
        iTop = img.offset().top;
        iLeft = img.offset().left;

        var bTop = imgBox.offset().top;
        var bLeft = imgBox.offset().left;
        // console.log(iTop, iLeft)
        // console.log(ratio, width, height)

        var startX, startY, endX, endY;
        // var divList = _this.divList;

        var drawing = false;
        var dragging = false;

        var dragStartX, dragStartY, dragDiv;

        // 根据divList渲染div
        for(var i = 0; i < _this.divList.length; i++) {
          var item = _this.divList[i];

          var div = document.createElement("div");
          div.className = "box";
          div.style.width = item.w * width + "px";
          div.style.height = item.h * height + "px";
          div.style.top = item.y * height + img.position().top + "px";
          div.style.left = item.x * width + img.position().left + "px";
          div.id = item.id;
          div.addEventListener("mousedown", handleDown);
          div.addEventListener("mousemove", handleMove);
          div.addEventListener("mouseup", handleUp);
          $(div).html("<span>" + item.label + "</span>");
          img.after(div);
        }

        img.mousedown(function (e) {
          // console.log(e)
          drawing = true;
          startX = e.pageX;
          startY = e.pageY;

          var div = document.createElement("div");
          div.className = "active";
          div.style.top = startY - bTop + "px";
          div.style.left = startX - bLeft + "px";
          // console.log(startX, iLeft)
          img.after(div);
        });

        $(document).mousemove(function (e) {
          // console.log(e.pageX <= width + iLeft, e.pageX >= iLeft)
          // if (e.pageX <= width + iLeft && e.pageX >= iLeft && e.pageY <= height + iTop && e.pageY >= iTop) {} else {
          //   $('.active').remove()
          //   drawing = false
          // }
          if(drawing && $(".active").length) {
            $(".active").width(e.pageX - startX);
            $(".active").height(e.pageY - startY);
          }
        });
        $(document).mouseup(function (e) {
          // console.log('document-mouseup')
          var active = $(".active");
          if(active.length) {
            drawing = false;

            if(active.width() <= 10 && active.height() <= 10) {
              active.remove();
              return false;
            }

            var div = document.createElement("div");
            div.className = "box";
            div.style.width = active.width() + "px";
            div.style.height = active.height() + "px";
            div.style.top = active.position().top + "px";
            div.style.left = active.position().left + "px";
            div.id = (startX.toString() + startY.toString()).replace(/\./g, "");
            div.addEventListener("mousedown", handleDown);
            div.addEventListener("mousemove", handleMove);
            div.addEventListener("mouseup", handleUp);
            if(_this.divList.length) {
              $(div).html(
                "<span>" +
                _this.divList[_this.divList.length - 1].label +
                "</span>"
              );
            }

            img.after(div);
            active.remove();

            endX = e.pageX;
            endY = e.pageY;

            _this.divList.push({
              x: (startX - iLeft) / width,
              y: (startY - iTop) / height,
              w: div.offsetWidth / width,
              h: div.offsetHeight / height,
              id: div.id,
              label: _this.divList.length
                ? _this.divList[_this.divList.length - 1].label
                : "",
            });
            // console.log(startX,startY,endX,endY)
            // _this.divList = divList;

            setTimeout(() => {
              $(".box").css("border", "1px dashed rgb(66, 104, 207, 0.5)");
              div.style.border = "2px solid rgb(94, 207, 66)";

              $(".cho_li .select").css("border", "none");
              $("." + div.id).css({
                border: "2px solid rgb(94, 207, 66)",
                "border-radius": "6px",
              });
            }, 50);
          }
          if($(dragDiv).length && e.target.className.indexOf("dragging") == -1) {
            console.log(999999);
            dragDiv.removeEventListener("mouseup", null);
            dragging = false;
            $(dragDiv).removeClass("dragging");
          }
        });

        // img.mousemove(function (e) {
        //   if (drawing && $(".active").length) {
        //     $(".active").width(e.pageX - startX);
        //     $(".active").height(e.pageY - startY);
        //   }
        // });

        img.mouseup(function (e) { });

        function handleDown (e) {
          console.log(e);
          dragging = true;
          if(e.target.className.indexOf("box") >= 0) {
            dragDiv = e.target;
          } else {
            dragDiv = e.path[1];
          }
          $(dragDiv).addClass("dragging");
          dragStartX = e.pageX;
          dragStartY = e.pageY;

          setTimeout(() => {
            $(".box").css("border", "1px dashed rgb(66, 104, 207, 0.5)");
            dragDiv.style.border = "2px solid rgb(94, 207, 66)";

            $(".cho_li .ivu-select").css("border", "none");
            $("." + dragDiv.id).css({
              border: "2px solid rgb(94, 207, 66)",
              "border-radius": "6px",
            });
          }, 50);
        }

        function handleMove (e) {
          // if(dragging && e.pageX <= width + iLeft && e.pageX >= iLeft && e.pageY <= height + iTop && e.pageY >= iTop) {
          if(dragging) {
            // 鼠标在图片范围内
            if(
              e.pageX <= width + iLeft &&
              e.pageX >= iLeft &&
              e.pageY <= height + iTop &&
              e.pageY >= iTop
            ) {
              var $dragDiv = $(dragDiv);
              var top = $dragDiv.position().top;
              var left = $dragDiv.position().left;
              var diffX = e.pageX - dragStartX;
              var diffY = e.pageY - dragStartY;

              var dWidth = $dragDiv.width() + 4;
              var dHeight = $dragDiv.height() + 4;

              var dTop = top + diffY;
              var dLeft = left + diffX;

              var iPTop = img.position().top;
              var iPLeft = img.position().left;

              dTop =
                dTop < iPTop ? iPTop : dTop > height - dHeight + iPTop ? height - dHeight + iPTop : dTop;
              dLeft =
                dLeft < iPLeft ? iPLeft : dLeft > width - dWidth + iPLeft ? width - dWidth + iPLeft : dLeft;

              dragDiv.style.top = dTop + "px";
              dragDiv.style.left = dLeft + "px";

              dragStartX = e.pageX;
              dragStartY = e.pageY;
            } else {
              console.log(11111111111);
              dragDiv.removeEventListener("mouseup", null);
              dragging = false;
              $(dragDiv).removeClass("dragging");
            }
            // console.log(dragStartX, diffX, dragStartX - iLeft - diffX)
          }
        }

        function handleUp (e) {
          if(!$(dragDiv).length) return false;
          // console.log("dragdiv", dragDiv);
          dragging = false;
          // console.log(e)
          var x = $(dragDiv).position().left - img.position().left;
          var y = $(dragDiv).position().top - img.position().top;
          console.log(x, y);
          _this.divList.forEach((item) => {
            // console.log(item.id, e.target.id)
            if(item.id == dragDiv.id) {
              item.x = x / width;
              item.y = y / height;
              item.id = (x.toString() + y.toString()).replace(/\./g, "");
            }
            console.log(item);
          });
          dragDiv.id = (x.toString() + y.toString()).replace(/\./g, "");
          $(dragDiv).removeClass("dragging");
          dragDiv = null;
        }
      }, 100);
    },
    addLabel () {
      this.labelList.push("");
    },
    inputAddLabel (idx, e) {
      this.$set(this.labelList, idx, e);
    },
    openSelect (item) {
      var { id } = item;
      $(".box").css("border", "1px dashed rgb(66, 104, 207, 0.5)");
      $("#" + id).css("border", "2px solid rgb(94, 207, 66)");

      $(".cho_li .select").css("border", "none");
      $("." + id).css({
        border: "2px solid rgb(94, 207, 66)",
        "border-radius": "6px",
      });
      // $()
    },
    selectLabel (item) {
      var { id, label } = item;
      label = label ? label : "";
      $("#" + id).html("<span>" + label + "</span>");
    },
    delLabel (idx) {
      this.labelList.splice(idx, 1);
    },
    delDiv (id) {
      this.divList = this.divList.filter((item) => item.id != id);
      $("#" + id).remove();
    },
    submit () {
      var item = this.divList.find((item) => !item.label);
      if(item) {
        this.$Message.error("请选择标签");
        return false;
      }
      console.log(this.divList);
    },
  },
};
</script>
<style lang="scss">
* {
  box-sizing: border-box;
}
.container {
  width: 1200px;
  height: calc(100vh - 60px);
  margin: 0 auto;
  text-align: center;
  background: #333;
  position: relative;
  padding-bottom: 110px;
  .unselect {
    -moz-user-select: none;
    -webkit-user-select: none;
    -ms-user-select: none;
    -khtml-user-select: none;
    user-select: none;
  }
  .img_box {
    // max-width: 710px;
    width: 60%;
    // height: 90%;
    height: 80%;
    position: absolute;
    top: 45%;
    left: 50%;
    transform: translate(-50%, -50%);
    // overflow-x: auto;
    // overflow-y: hidden;
  }

  #img {
    // max-width: 100%;
    // height: 100%;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
  }

  #img:hover {
    cursor: crosshair;
  }

  .active,
  .box {
    background: rgba(66, 104, 207, 0.3);
    position: absolute;
  }

  .box {
    border: 1px dashed rgb(66, 104, 207, 0.5);
    // border: 1px dashed rgba(94, 207, 66, 0.5);
    cursor: move;
  }
  .box span {
    // background: #aaa;
    font-size: 12px;
    background: rgba(0, 0, 0, 0.2);
    color: #fff;
    position: absolute;
    bottom: 0;
    left: 0;
  }
  .choose_label {
    float: right;
    margin-right: 30px;
  }
  .choose_label,
  .add_label {
    max-height: 100%;
    padding-top: 50px;
    overflow-y: auto;
  }
  .delete {
    width: 16px;
    height: 16px;
    margin-left: 16px;
    vertical-align: middle;
    cursor: pointer;
  }
  .add_li,
  .cho_li {
    line-height: 40px;
    height: 40px;
    // vertical-align: middle;
  }
  .add_label {
    float: left;
    margin-left: 30px;

    .add {
      margin: 20px 0;
    }
  }
}
</style>
