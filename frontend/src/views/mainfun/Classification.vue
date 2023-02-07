<template>
  <div>
    <Tabinfor>
      <template #left>
        <div id="sub-title">
        关键部位快速精确毁伤评估<i class="iconfont icon-dianji"/>
        </div>
      </template>
    </Tabinfor>
    <el-divider />
    <p>
      请上传包含<span class="go-bold">船舰图片的文件夹</span><i class="iconfont icon-wenjianjia" />或者<span class="go-bold">图片</span>
    </p>
    <el-row
      type="flex"
      justify="center"
    >
      <el-col :span="24">
        <el-card style="border: 4px dashed var(--el-border-color)">
          <div
            v-if="fileList.length"
            class="clear-queue"
          >
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
            <div

              class="el-upload__tip"
            >
              只能上传一张或多张图片，请在下方上传文件夹
            </div>
          </el-upload>
          <!-- <el-row justify="center">
            <input
              id="folder"
              ref="uploadFile"
              type="file"
              webkitdirectory
              directory
              multiple
              @change="uploadMore()"
            >
            <i
              class="iconfont icon-wenjianshangchuan"
              @click="fileClick"
            >上传文件夹</i>
          </el-row> -->

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
          </el-row> -->

          <el-row
            justify="center"
            align="middle">
            <el-col :span="12">
              <div class="handle-button">
                <el-button
                  type="primary"
                  class="btn-animate btn-animate__shiny"
                  @click="upload('孪生分类','classification')"
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
    <classification_imgShow
      :img-arr = "imgArr"/>
    
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
      <Analysis_Show_3
        :img-arr = "analyse_img_list"/>

    <Tabinfor>
      <template #left>
        <div id="sub-title"> 相关毁伤评估信息<i class="iconfont icon-dianji"/> </div>
      </template>
      <template #right>
          <div id="sub-title"> 原图宽高尺寸：{{size}} </div>
      </template>
    </Tabinfor>
    <el-divider />
    <el-row justify="center"
      align="middle">
      <el-col :span="8">
        <el-table
          :data="tableData"
          height="200"
          border
          style="width: 100%">
          <el-table-column
            prop="id"
            label="ID"
            width="50">
          </el-table-column>
          <el-table-column
            prop="predict_class_1"
            label="预测损伤等级"
            width="150">
          </el-table-column>
          <el-table-column
            prop="probability_1"
            label="置信度"
            width="100">
          </el-table-column>
          <el-table-column
            prop="time_1"
            label="推理时间(单位:毫秒)"
            width="100">
          </el-table-column>
          </el-table>
      </el-col>

      <el-col :span="8">
        <el-table
          :data="tableData"
          height="200"
          border
          style="width: 100%">
          <el-table-column
            prop="id"
            label="ID"
            width="50">
          </el-table-column>
          <el-table-column
            prop="predict_class_2"
            label="预测损伤等级2"
            width="150">
          </el-table-column>
          <el-table-column
            prop="probability_2"
            label="置信度"
            width="100">
          </el-table-column>
          <el-table-column
            prop="time_2"
            label="推理时间(单位:毫秒)"
            width="100">
          </el-table-column>
          </el-table>
      </el-col>

      <el-col :span="8">
        <el-table
          :data="tableData"
          height="200"
          border
          style="width: 100%">
          <el-table-column
            prop="id"
            label="ID"
            width="50">
          </el-table-column>
          <el-table-column
            prop="predict_class_3"
            label="预测损伤等级3"
            width="150">
          </el-table-column>
          <el-table-column
            prop="probability_3"
            label="置信度"
            width="100">
          </el-table-column>
          <el-table-column
            prop="time_3"
            label="推理时间(单位:毫秒)"
            width="100">
          </el-table-column>
          </el-table>
      </el-col>
    </el-row>
    
    <el-divider />
    <el-table
    :data="tableAP"
    height="300"
    border
    style="width: 100%">
    <el-table-column
      prop="ap"
      label="识别准确率"
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
import {createSrc, imgUpload,getCustomModel} from "@/api/upload";
import {historyGetPage} from "@/api/history";
import {upload} from "@/utils/getUploadImg";
import classification_imgShow from '@/components/classification_imgShow'
import Analysis_Show_3 from "@/components/Analysis_Show_3";
import Tabinfor from "@/components/Tabinfor";
import Bottominfor from "@/components/Bottominfor";
import MyVueCropper from "@/components/MyVueCropper";
import global from '@/global'
export default {
  name: "Classification",
  components: {
    Tabinfor,
    Bottominfor,
    MyVueCropper,
    classification_imgShow,
    Analysis_Show_3
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
      before:[],
      fileimg: "",
      file: {},
      isNotCut: true,
      cutVisible: false,
      funtype: "孪生分类",
      scrollTop: "",
      fit: "fill",
      fileList: [],
      uploadSrc: {
        list: [],
        model_path:''
      },
      modelPathArr:[],
      imgArr:[],
      tableData: [],
      size: "",
      analyse_img_list:[],
      networksrc:"",
      tableAP:[],
    };
  },
  updated() {
    // console.log("这是updated函数的内容");
    console.log(this.imgArr);
    // this.tableData.forEach((item,index)=>{
    //   for (const key in item) {
    //     console.log(typeof(item[key]))
    //     console.log("item[key]",item[key]);//值
    //     // console.log("key",key);//键
    //   }
    // })
  },
  mounted() {
    // console.log("这是mounted函数的内容");
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
    // this.getCustomModel('classification').then((res)=>{
    //   this.modelPathArr = res.data.data
    //   this.uploadSrc.model_path = this.modelPathArr[0]?.model_path
    // }).catch((rej)=>{})
    this.networksrc = global.BASEURL+"/data1/lkh/GeoView-release-0.1/backend/static/test_show/network/network.png"
  },
  methods: {
    imgUpload,
    getCustomModel,
    historyGetPage,
    createSrc,
    upload,
    checkUpload() {
      this.isUpload = this.beforeImg.length !== 0;
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
      this.getUploadImg("孪生分类");
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
        this.fileimg = window.URL.createObjectURL(new Blob([file]));}
    },
    select() {
      // this.isNotCut = this.$refs.cut.checked;
    },
    load_picture(){
        var split_name = this.imgArr[0]["before_img"].split('/')
        var fname = split_name[split_name.length-1].replace("jpg","png")
        this.analyse_img_list = []
        this.analyse_img_list.push({
                "id":1,
                "type":"xxxx",
                "heatmap1": global.BASEURL+"/data1/lkh/GeoView-release-0.1/backend/static/test_show/heatmap_easy/heatmap_"+fname,
                "heatmap2": global.BASEURL+"/data1/lkh/GeoView-release-0.1/backend/static/test_show/heatmap_mid/heatmap_"+fname,
                "heatmap3": global.BASEURL+"/data1/lkh/GeoView-release-0.1/backend/static/test_show/heatmap_hard/heatmap_"+fname,
                // "netmap": global.BASEURL+"/data1/lkh/GeoView-release-0.1/backend/static/test_show/cnn.png",
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
.img-index {
  align-items: center;
  display: flex;
  flex-direction: column;
  justify-content: space-evenly;
  flex-wrap: wrap;
}
.index-number {
  font-family: Yu Gothic Medium;
  font-style: oblique;
  font-size: 30px;
  margin-left: 5px;
  margin-right: 10px;
}
.img-infor {
  text-align: center;
  font-size: 18px;
  margin-top: 5px;
  margin-bottom: 10px;
  width: 256px;
  height: 30px;
  font-weight: 500;
  font-family: Microsoft JhengHei UI, sans-serif;
}
.custom-pic{
  width: 256px;
  height: 256px;
}
.el-radio /deep/{
  height: 62px;
}
</style>
