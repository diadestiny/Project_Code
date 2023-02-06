<template>
  <div>
    <Tabinfor>
      <template #left>
        <div id="sub-title">
          海面远距目标精确识别<i class="iconfont icon-dianji" />
        </div>
      </template>
    </Tabinfor>
    <el-divider />
    <p>
      请上传<span class="go-bold">相关图片的文件夹</span><i class="iconfont icon-wenjianjia" />或者<span
        class="go-bold"
      >图片</span>
    </p>
    <el-row
      type="flex"
      justify="center"
    >
      <el-col :span="24">
        <el-card style="border: 4px dashed var(--el-border-color)">
          <div
            v-if="fileList.length"
            class="clear-queue">
            <el-button
              type="primary"
              class="btn-animate2 btn-animate__surround"
              @click="clearQueue"
            >
              清空图片
            </el-button>
          </div>
          <el-upload
            ref="upload"
            v-model:file-list="fileList"
            class="upload-card"
            drag
            action="#"
            multiple
            :auto-upload="false"
            @change="beforeUpload(fileList[fileList.length - 1].raw)"
          >
            <i class="iconfont icon-yunduanshangchuan" />
            <div class="el-upload__text">
              将文件拖到此处，或<em>点击上传</em>
            </div>
            <div class="el-upload__tip">
               只能上传一张或多张图片，请在下方上传文件夹
            </div>
          </el-upload>
          <!-- <el-row justify="center">
            <p>
              <label class="prehandle-label container">
                <input
                  ref="cut"
                  type="checkbox"

                  @change="select()"
                >
                <span class="checkmark" />
                <span class="go-bold label-words">上传时编辑图片</span><i
                  class="iconfont icon-crop-full"
                />
              </label>
            </p>
          </el-row>   -->
          <el-row
            justify="center"
            align="middle">
            <el-col :span="12">
          <div class="handle-button">
            <el-button
              type="primary"
              class="btn-animate btn-animate__shiny"
              @click="upload('目标检测','object_detection')"
            >
              开始处理
            </el-button>
          </div>
         </el-col>
         <el-col :span="12">
            <div class="handle-button">
              <el-button
                type="primary"
                class="btn-animate btn-animate__shiny"
                @click="load_picture()">
                模型分析
              </el-button>
            </div>
          </el-col>
          </el-row>
          
          <!-- <el-divider v-if="!uploadSrc.prehandle" /> -->
        </el-card>
      </el-col>
    </el-row>
    <Tabinfor>
      <template #left>
        <div
          id="sub-title"
        >
          结果图预览<i
            class="iconfont icon-dianji"
          />
        </div>
      </template>
    </Tabinfor>
    <el-divider />
    <Tabinfor>
      <template #left>
        <p>
          <span class="go-bold">点击图片</span>即可预览
          <i
            class="iconfont icon-duigou"
          />
          <span><span class="go-bold">滑轮滚动</span>即可放大缩小</span>
        </p>
      </template>
      <template #mid>
        <p v-if="isUpload">
          <i
            class="iconfont icon-dabaoxiazai"
            @click="goCompress('目标检测')"
          >结果图打包</i>
        </p>
      </template>
      <template #right>
        <span class="go-bold"><i
          class="iconfont icon-shuaxin"
          style="padding-right:55px"
          @click="getMore"
        ><span class="hidden-sm-and-down">点击刷新</span></i></span>
      </template>
    </Tabinfor>
    <el-dialog
      v-model="cutVisible"
      :modal="false"
      title="编辑"
      width="75%"
      top="0"
    >
      <MyVueCropper
        :fileimg="fileimg"
        :funtype="funtype"
        :file="file"
        :child_prehandle="uploadSrc.prehandle"
        :child_denoise="uploadSrc.denoise"
        :child-model-path="uploadSrc.model_path"
        @cut-changed="notvisible"
        @child-refresh="getMore"
      />
    </el-dialog>
    <ImgShow
      :img-arr="imgArr"/>
    <Tabinfor>
        <template #left>
          <div id="sub-title">
            推理分析预览<i class="iconfont icon-dianji" />
          </div>
        </template>
      </Tabinfor>
      <el-divider />
      <Tabinfor>
        <template #left>
          <p>
            <span class="go-bold">点击图片</span>即可预览
            <i
              class="iconfont icon-duigou"
            />
            <span><span class="go-bold">滑轮滚动</span>即可放大缩小</span>
          </p>
        </template>
        <template #right>
          <span class="go-bold"><i
            class="iconfont icon-shuaxin"
            style="padding-right:55px"
            @click="getMore"
          ><span class="hidden-sm-and-down">点击刷新</span></i></span>
        </template>
      </Tabinfor>
      <Analysis_Show
        :img-arr = "analyse_img_list"/>

    <Tabinfor>
      <template #left>
        <div id="sub-title"> 相关检测信息<i class="iconfont icon-dianji"/> </div>
      </template>
      <template #right>
          <div id="sub-title"> 原图宽高尺寸：{{size}} </div>
      </template>
    </Tabinfor>
    <el-divider />
    <el-table
    :data="tableData"
    height="300"
    border
    style="width: 100%">
    <el-table-column
      prop="id"
      label="ID"
      width="50">
    </el-table-column>
    <el-table-column
      prop="class"
      label="类别"
      width="120">
    </el-table-column>
    <el-table-column
      prop="bbox"
      label="目标位置(x1,y1,x2,y2)"
      width="250">
    </el-table-column>
    <el-table-column
      prop="size"
      label="目标尺寸(宽x高)"
      width="250">
    </el-table-column>
    <el-table-column
      prop="score"
      label="置信度"
      width="100">
    </el-table-column>
    <el-table-column
      prop="time"
      label="推理时间(单位:毫秒)"
      width="100">
    </el-table-column>
    </el-table>
    <el-divider />
    <el-table
    :data="tableAP"
    height="300"
    border
    style="width: 100%">
    <el-table-column
      prop="class"
      label="类别"
      width="120">
    </el-table-column>
    <el-table-column
      prop="ap"
      label="平均预测准确率"
      width="150">
    </el-table-column>
    </el-table>
    <Tabinfor>
      <template #left>
        <div id="sub-title"> 模型架构图<i class="iconfont icon-dianji"/> </div>
      </template>
    </Tabinfor>
    <el-divider />
    <div>
      <el-image
        ref="tableTab"
        class="img-display"
        :src="networksrc"
        :fit="fit"
        :lazy="true"
        :preview-src-list="[networksrc]"
        :preview-teleported="true"
      />
    </div>
    <Bottominfor />
  </div>
</template>

<script>
import {atchDownload, downloadimgWithWords, getImgArrayBuffer} from "@/utils/download.js";
import {createSrc, imgUpload,getCustomModel} from "@/api/upload";
import {historyGetPage} from "@/api/history";
import {goCompress, upload} from "@/utils/getUploadImg";
import {selectClahe, selectFilter, selectSharpen, selectSmooth,} from "@/utils/preHandle";
import ImgShow from "@/components/ImgShow";
import Analysis_Show from "@/components/Analysis_Show";
import Tabinfor from "@/components/Tabinfor";
import Bottominfor from "@/components/Bottominfor";
import MyVueCropper from "@/components/MyVueCropper";
import global from '@/global'
export default {
  name: "Detectobjects",
  components: {
    ImgShow,
    Analysis_Show,
    Tabinfor,
    Bottominfor,
    MyVueCropper,
  },
  beforeRouteEnter(to, from, next) {
    next((vm) => {
      document.querySelector(".el-main").scrollTop = 0;
    });
  },
  data() {
    return {
      isUpload:true,
      canUpload:true,
      claheImg:[],
      sharpenImg:[],
      before:[],
      fileimg: "",
      file: {},
      isNotCut: true,
      cutVisible: false,
      funtype: "目标检测",
      scrollTop: "",
      fit: "fill",
      networksrc:"",
      fileList: [],
      uploadSrc: {
        list: [],
        prehandle: 0,
        denoise: 0,
        model_path:''
      },
      modelPathArr:[],
      prePhoto:{
        list:[],
        prehandle:0,
        type:4
      },
      imgArr:[],
      tableData: [],
      tableAP:[],
      size: "",
      analyse_img_list:[]
    };
  },
  updated() {
    // this.tableData.forEach((item,index)=>{
    //   for (const key in item) {
    //     console.log(typeof(item[key]))
    //     console.log("item[key]",item[key]);//值
    //     // console.log("key",key);//键
    //   }
    // })
  },
  mounted() {
  },
  watch:{
    uploadSrc:{
      handler(newVal,oldVal){
        this.uploadSrc = newVal
      },
      deep:true,
      immediate:true
    }
  },
  created() {
    this.networksrc = global.BASEURL+"/data1/lkh/GeoView-release-0.1/backend/static/test_detection/network.png"
  },
  methods: {
    getImgArrayBuffer,
    atchDownload,
    downloadimgWithWords,
    imgUpload,
    getCustomModel,
    historyGetPage,
    createSrc,
    upload,
    goCompress,
    selectSharpen,
    selectFilter,
    selectSmooth,
    selectClahe,
    checkUpload() {
      this.isUpload = this.afterImg.length !== 0;
    },
    clearQueue() {
      this.fileList = [];
      this.$message.success("清除成功");
    },
    notvisible() {
      this.cutVisible = false;
      this.fileList = [];
    },
    getMore() {
    },
    uploadMore() {
            this.beforeUpload(...this.$refs.uploadFile.files)
        if(this.canUpload){
          this.fileList.push(...this.$refs.uploadFile.files);
        }else{
          setTimeout(() => {
              this.$message.error('检测到您上传的文件夹内存在不符合规范的图片类型')
          }, 1000);
        
        }
    },
    fileClick() {
      document.querySelector("#folder").click();
    },
    beforeUpload(file) {
        // this.cutVisible = this.$refs.cut.checked;
        const fileSuffix = file.name.substring(file.name.lastIndexOf(".") + 1)
        const whiteList = ['jpg','jpeg','png','JPG','JPEG']
        if (whiteList.indexOf(fileSuffix) === -1) {
            this.$message.error("只允许上传jpg, jpeg, png, JPG, 或JPEG格式,请重新上传");
            this.fileList= []
            this.canUpload = false
            this.cutVisible = false;
        }
        else{
            this.canUpload = true
            this.fileimg = window.URL.createObjectURL(new Blob([file]));
      }
    },
    select() {
      // this.isNotCut = this.$refs.cut.checked;
    },
    load_picture(){
            var split_name = this.imgArr[0]["after_img"].split('/')
            var fname = split_name[split_name.length-1]
            this.analyse_img_list = []
            this.analyse_img_list.push({
              "id":1,
              "type":"目标检测",
              "heatmap": global.BASEURL+"/data1/lkh/GeoView-release-0.1/backend/static/test_detection/heatmap/heatmap3_"+fname,
              // "netmap": global.BASEURL+"/data1/lkh/GeoView-release-0.1/backend/static/test_detection/network.png",
            });
        
        // console.log(this.img_list);
      },
  },
};
</script>

<style lang="less" scoped>
* {
  font-family: SimHei sans-serif;
}
#sub-title{
  font-size: 25px;
}
#sub-title:hover:after {
  left: 0%;
  right: 0%;
  width: 220px;
}
.clear-queue {
  position: absolute;
  left: 5px;
  top: 10%;
  z-index: 100;
}
.el-radio /deep/{
  height: 62px;
}
</style>

