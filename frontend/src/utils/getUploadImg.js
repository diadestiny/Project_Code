import { historyGetPage } from "@/api/history"
import global from '@/global'
import {showFullScreenLoading} from "@/utils/loading";

function getUploadImg(type) {
  // historyGetPage(1, 20, type).then((res) => {
  //   this.imgArr = res.data.data.forEach((item)=>{
  //     item['before_img'] = global.BASEURL+item.before_img
  //     item['after_img'] = global.BASEURL+item.after_img
  //   })
    
  //   this.imgArr = res.data.data
  //   this.isUpload = this.imgArr.length !== 0;
  // }).catch((rej)=>{})
}

function goCompress(type,num) {
  this.historyGetPage(1, num, type).then((res) => {
    this.atchDownload(
        res.data.data.map((item) => {
          return { after_img: item.after_img, id: item.id };
        })
    );
  }).catch((rej)=>{});
}

function upload(type,funUrl) {
  
  if (this.fileList.length === 0) {
    this.$message.error("请上传图片！");
  } else {
    let formData = new FormData();
    let _this = this;
    for (const item of this.fileList) {
      formData.append("files", item) || formData.append('files', item.raw);
      formData.append("type", type);
    }
    this.createSrc(formData).then((res) => {
      this.uploadSrc.list = res.data.data.map((item) => {
        return item.src;
      });
        this.imgUpload(this.uploadSrc,funUrl).then((res) => {
          this.fileList = []
          this.$message.success("上传成功！");
          this.imgArr = res.data.data["imgArr"].forEach((item)=>{
            item['before_img'] = global.BASEURL+item['before_img']
            item['after_img'] = global.BASEURL+item['after_img']
          });
          this.imgArr = res.data.data["imgArr"];
          this.isUpload = this.imgArr.length !== 0;
          this.tableData = res.data.data["tableData"];
          this.tableAP = res.data.data["tableAP"];
          this.size = res.data.data["size"];
          if(type=="目标定位"){
            this.outArr = res.data.data["outArr"].forEach((item)=>{
              item['out_main_img'] = global.BASEURL+item['out_main_img']
              item['out_side_img'] = global.BASEURL+item['out_side_img']
            });
            this.outArr = res.data.data["outArr"];
            this.side_tableData = res.data.data["side_tableData"];
            this.side_tableAP = res.data.data["side_tableAP"];
            // console.log(this.outArr)
          }
          // this.getMore()
        });
      if (this.uploadSrc.list.length >= 10 && type!=='场景分类') {
        this.$confirm("上传图片过多，是否压缩?", "提示", {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning",
        })
          .then(() => {
            showFullScreenLoading('#load','压缩中')
            this.goCompress(type,this.uploadSrc.list.length)
          }).catch(() => {

        })
      }
      _this.$refs.upload.clearFiles();
    }).catch((rej)=>{})
  }
}


export { getUploadImg, goCompress, upload }