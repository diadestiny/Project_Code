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
        <div id="sub-title"> 已知相关船舰信息<i class="iconfont icon-dianji"/> </div>
      </template>
      </Tabinfor>
      <el-divider />
        <el-table
          :data="inputData2"
          height="300"
          border
          style="width: 100%">
          <el-table-column
            prop="id"
            label="ID"
            width="50">
          </el-table-column>
          <!-- <el-table-column
            prop="biaoshifu"
            label="标识符"
            width="200">
          </el-table-column> -->
          <el-table-column
            prop="jingdu"
            label="经度"
            width="120">
          </el-table-column>
          <el-table-column
            prop="weidu"
            label="纬度"
            width="120">
          </el-table-column>
          <!-- <el-table-column
            prop="height"
            label="高度"
            width="100">
          </el-table-column> -->
          <el-table-column
            prop="date"
            label="日期"
            width="120">
          </el-table-column>
          <el-table-column
            prop="time"
            label="时间"
            width="120">
          </el-table-column>
          <!-- <el-table-column
            prop="encode"
            label="类型编码"
            width="100">
          </el-table-column> -->
        </el-table>
      <!-- <p>
        请上传包含<span class="go-bold">船舰图片的文件夹</span><i class="iconfont icon-wenjianjia" />或者<span class="go-bold">图片</span>
      </p> -->
      <el-row >
          <el-col :span="8">
            <div class="handle-button">
              <el-upload
                ref="upload"
                v-model:file-list="fileList"
                action="#"
                multiple
                :auto-upload="false"
              >
                <el-button type="primary" class="btn-animate btn-animate__shiny">选取文件</el-button>
              </el-upload>
             
            </div>
          </el-col>
          <el-col :span="8">
            <div class="handle-button">
                <el-button
                  type="primary"
                  class="btn-animate btn-animate__shiny"
                  @click="upload_stiuation('态势推理','situation')">
                  轨迹生成
                </el-button>
            </div>
          </el-col>
          <el-col :span="8">
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
            轨迹预览<i
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
      <situation_imgShow
        :img-arr = "img_list"/>
        <Tabinfor>
        <template #left>
          <div
            id="sub-title"
          >
            推理结果预览<i
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
      <situation_imgShow2
        :img-arr = "img_list_2"/>
      
      <el-divider/>
      <!-- <Tabinfor>
        <template #left>
            <div id="sub-title"> 态势预测图<i class="iconfont icon-dianji"/> </div>
          </template>
        </Tabinfor>
        <el-divider />
        <div class="gif">
          <el-image
            ref="tableTab"
            class="img-display"
            :src="gifsrc"
            :fit="fit"
            :lazy="true"
            :preview-src-list="[gifsrc]"
            :preview-teleported="true"
          />
        </div> -->

      <Tabinfor> 
      <template #left>
        <div id="sub-title"> 相关态势预测信息<i class="iconfont icon-dianji"/> </div>
      </template>
      </Tabinfor>
      <el-divider />
      <el-table
      :data="outputData"
      height="300"
      border
      style="width: 100%">
      <el-table-column
        prop="id"
        label="ID"
        width="50">
      </el-table-column>
      <el-table-column
        prop="pre_jingdu"
        label="预测经度"
        width="120">
      </el-table-column>
      <el-table-column
        prop="pre_weidu"
        label="预测纬度"
        width="120">
      </el-table-column>
      <el-table-column
        prop="real_jingdu"
        label="真实经度"
        width="120">
      </el-table-column>
      <el-table-column
        prop="real_weidu"
        label="真实纬度"
        width="120">
      </el-table-column>
      <el-table-column
        prop="dis"
        label="距离(单位:米)"
        width="150">
      </el-table-column>
      <el-table-column
        prop="flag"
        label="是否预测正确"
        width="120">
      </el-table-column>
      <el-table-column
        prop="time"
        label="推理时间(单位:毫秒)"
        width="200">
      </el-table-column>
    </el-table>
    <el-divider />
      <el-table
      :data="ap_data"
      height="300"
      border
      style="width: 100%">
      <el-table-column
        prop="ap"
        label="预测准确率"
        width="100">
      </el-table-column>
    </el-table>
    
    <Tabinfor>
    <template #left>
        <div id="sub-title"> 模型架构图<i class="iconfont icon-dianji"/> </div>
      </template>
    </Tabinfor>
    <el-divider />
    <div >
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
  import {upload,upload_stiuation} from "@/utils/getUploadImg";
  import {getSituation} from "@/api/upload";
  import situation_imgShow from '@/components/situation_imgShow'
  import situation_imgShow2 from '@/components/situation_imgShow2'
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
      situation_imgShow2,
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
        networksrc:"",
        gifsrc:"",
        // inputData:[{
        //   id:'1',
        //   timestamp: '2074293900',
        //   longitude: '116.801289',
        //   latitude: '39.950773',
        //   height:'10000',
        //   speed:'15.18338756',
        //   angle:'214.6854958',
        //   encode:'2009-04-15',
        //   time:'00:04:06'
        // },
        // {
        //   id:'2',
        //   timestamp: '2074299030',
        //   longitude: '136.9361255',
        //   latitude: '31.38977628',
        //   height:'10000',
        //   speed:'15.19845853',
        //   angle:'214.2785259',
        //   encode:'2010101'
        // },
        // {
        //   id:'3',
        //   timestamp: '2074306200',
        //   longitude: '136.362676',
        //   latitude: '30.53955996',
        //   height:'10000',
        //   speed:'15.21203915',
        //   angle:'213.7246856',
        //   encode:'2010101'
        // },
        // {
        //   id:'4',
        //   timestamp: '2074315830',
        //   longitude: '135.6075397',
        //   latitude: '29.39286647',
        //   height:'10000',
        //   speed:'15.21621424',
        //   angle:'213.0162978',
        //   encode:'2010101'
        // }],
        inputData2:[],
        outputData:[],
        ap_data:[],
        img_list:[],
        img_list_2:[],
        temp_name:""
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
      this.networksrc = global.BACKEND_URL+ "test_situation/network.png"
      //  this.gifsrc = global.BACKEND_URL+ "test_situation/t_zimu.gif"
    },
    methods: {
      imgUpload,
      getCustomModel,
      historyGetPage,
      createSrc,
      upload,
      upload_stiuation,
      getSituation,
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
        var temp_name = this.fileList[0].name.replace("txt","png")
        this.img_list.push({
                "id":1,
                "type":"态势预测",
                "img_path": global.BACKEND_URL+ "test_situation/"+temp_name
        });
        // console.log(this.img_list);
      },
      inference(){
        // var action_list = ["预警机升空","预警机飞行","战斗机升空","战斗机飞行","预警机警戒","战斗机攻击"];
        // var index = Math.round(Math.random()*(0-5) + 5);
        // // console.log(index)
        // var probability = (Math.random()*(80-96) + 96)/100;
        // // console.log(probability.toFixed(3))
        // var time = Math.round(Math.random()*(600-990) + 990);
        // this.tableData=[];
        // this.tableData.push({
        //         "id":1,
        //         "action":action_list[index],
        //         "probability": probability.toFixed(3),
        //         "time":time,
        // })
        // this.inputData2 = []
        this.gifsrc = global.BACKEND_URL+ "test_situation/t_zimu.gif"
        this.outputData = []
        this.ap_data = []
        this.getSituation("situation",this.temp_name).then((res) => {
            var temp = res.data.data["imgArr"];
            for(var i=0;i<temp.length;i++){
              this.outputData.push({"id":temp[i]["id"],"pre_jingdu":temp[i]["pre_jingdu"],"pre_weidu":temp[i]["pre_weidu"],"real_jingdu":temp[i]["real_jingdu"],"real_weidu":temp[i]["real_weidu"],"dis":temp[i]["dis"],
                                    "flag":temp[i]["flag"],"time":temp[i]["time"]})
            }
              this.ap_data.push({"ap":res.data.data["ap"][0]["acc"]})
          });
          // console.log(this.inputData2)
          var temp_png_name = this.temp_name.replace("txt","png")
          this.img_list_2 = []
          this.img_list_2.push({
                  "id":1,
                  "type":"态势预测",
                  "img_path": global.BACKEND_URL+ "test_situation/output/"+temp_png_name
          });
          // console.log(temp_png_name)
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
  .gif{
    display: flex;
    justify-content: center;  //弹性盒子对象在主轴上的对齐方式
    align-items: center;      //定义flex子项在flex容器的当前行的侧轴(纵轴)方向上的对齐方式。
    // background-color:#00a0e9;
    // height:200px;

  }
  </style>
  