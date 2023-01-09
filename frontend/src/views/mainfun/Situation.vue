<template>
    <div>
      <Tabinfor>
        <template #left>
          <div id="sub-title">
            知识和数据融合驱动态势预测<i class="iconfont icon-dianji"/>
          </div>
        </template>
      </Tabinfor>
      <el-divider />
      <Tabinfor>
      <template #left>
        <div id="sub-title"> 已知相关飞机信息<i class="iconfont icon-dianji"/> </div>
      </template>
      </Tabinfor>
      <el-divider />
      <el-table
      :data="inputData"
      height="300"
      border
      style="width: 100%">
      <el-table-column
        prop="id"
        label="ID"
        width="50">
      </el-table-column>
      <el-table-column
        prop="timestamp"
        label="时间戳"
        width="150">
      </el-table-column>
      <el-table-column
        prop="longitude"
        label="经度"
        width="120">
      </el-table-column>
      <el-table-column
        prop="latitude"
        label="纬度"
        width="120">
      </el-table-column>
      <el-table-column
        prop="height"
        label="高度"
        width="100">
      </el-table-column>
      <el-table-column
        prop="speed"
        label="速度"
        width="120">
      </el-table-column>
      <el-table-column
        prop="angle"
        label="航向角"
        width="120">
      </el-table-column>
      <el-table-column
        prop="encode"
        label="类型编码"
        width="100">
      </el-table-column>
    </el-table>
      <!-- <p>
        请上传包含<span class="go-bold">船舰图片的文件夹</span><i class="iconfont icon-wenjianjia" />或者<span class="go-bold">图片</span>
      </p> -->
        <el-row >
          <el-col :span="12">
            <div class="handle-button">
              <el-button
                type="primary"
                class="btn-animate btn-animate__shiny"
                @click="load_picture()">
                加载图谱
              </el-button>
            </div>
          </el-col>
          <el-col :span="12">
            <div class="handle-button">
              <el-button
                type="primary"
                class="btn-animate btn-animate__shiny"
                @click="inference()">
                态势推理
              </el-button>
            </div>
          </el-col>
      </el-row>      
      <Tabinfor>
        <template #left>
          <div
            id="sub-title"
          >
            图谱预览<i
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
      <situation_imgShow
        :img-arr = "img_list"/>
      <Tabinfor>
      <template #left>
        <div id="sub-title"> 相关态势预测信息<i class="iconfont icon-dianji"/> </div>
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
        prop="action"
        label="预测行为"
        width="150">
      </el-table-column>
      <el-table-column
        prop="probability"
        label="准确率"
        width="100">
      </el-table-column>
      <el-table-column
        prop="time"
        label="推理时间(单位:毫秒)"
        width="100">
      </el-table-column>
    </el-table>
      <Bottominfor />
    </div>
  </template>
  <script>
  import {createSrc, imgUpload,getCustomModel} from "@/api/upload";
  import {historyGetPage} from "@/api/history";
  import {upload} from "@/utils/getUploadImg";
  import situation_imgShow from '@/components/situation_imgShow'
  import classification_imgShow from '@/components/classification_imgShow'
  import Tabinfor from "@/components/Tabinfor";
  import Bottominfor from "@/components/Bottominfor";
  import MyVueCropper from "@/components/MyVueCropper";
  import global from '@/global'
  export default {
    name: "Situation",
    components: {
      Tabinfor,
      Bottominfor,
      MyVueCropper,
      situation_imgShow,
      classification_imgShow
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
        funtype: "态势推理",
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
        inputData:[{
          id:'1',
          timestamp: '2074293900',
          longitude: '137.352373',
          latitude: '31.995839',
          height:'10000',
          speed:'15.18338756',
          angle:'214.6854958',
          encode:'2010101'
        },
        {
          id:'2',
          timestamp: '2074299030',
          longitude: '136.9361255',
          latitude: '31.38977628',
          height:'10000',
          speed:'15.19845853',
          angle:'214.2785259',
          encode:'2010101'
        },
        {
          id:'3',
          timestamp: '2074306200',
          longitude: '136.362676',
          latitude: '30.53955996',
          height:'10000',
          speed:'15.21203915',
          angle:'213.7246856',
          encode:'2010101'
        },
        {
          id:'4',
          timestamp: '2074315830',
          longitude: '135.6075397',
          latitude: '29.39286647',
          height:'10000',
          speed:'15.21621424',
          angle:'213.0162978',
          encode:'2010101'
        }],
        img_list:[]
      }
      
    },
    updated() {
      // console.log("这是updated函数的内容");
      // console.log(this.imgArr);
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
        this.getUploadImg("态势推理");
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
        this.cutVisible = this.$refs.cut.checked;
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
        this.isNotCut = this.$refs.cut.checked;
      },
      load_picture(){
        this.img_list.push({
                "id":1,
                "type":"态势预测",
                "img_path": global.BASEURL+"/data1/lkh/GeoView-release-0.1/backend/static/test_situation/situation1.png"
        });
        // console.log(this.img_list);
      },
      inference(){
        var action_list = ["预警机升空","预警机飞行","战斗机升空","战斗机飞行","预警机警戒","战斗机攻击"];
        var index = Math.round(Math.random()*(0-5) + 5);
        console.log(index)
        var probability = (Math.random()*(80-96) + 96)/100;
        console.log(probability.toFixed(3))
        var time = Math.round(Math.random()*(600-990) + 990);
        this.tableData=[];
        this.tableData.push({
                "id":1,
                "action":action_list[index],
                "probability": probability.toFixed(3),
                "time":time,
        })
        console.log(this.tableData)
      }
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
  