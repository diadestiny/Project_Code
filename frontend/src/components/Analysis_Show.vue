<template>
  <el-card style="margin-bottom: 10px">
    <el-empty
      v-if="childImgArr.length === 0"
      :image-size="200"
    />
    <div class="img-display-box">
      <div
        v-for="(item,index) in childImgArr"
        :key="index"
        class="img-display-item"
      >
        <!-- <el-divider class="img-divider">
          第<span class="index-number">{{ item.id }}</span>组
        </el-divider> -->
        <div>
          <el-image
            ref="tableTab"
            class="img-display"
            :src="item.heatmap"
            :fit="fit"
            :lazy="true"
            :preview-src-list="[item.heatmap]"
            :preview-teleported="true"
          />
         
          <div class="img-infor">
            <span id="myspan1">热力图</span>
          </div>
        </div>
        
        <!-- <div>
          <el-image
            ref="tableTab"
            class="img-display"
            :src="item.before_img"
            :fit="fit"
            :lazy="true"
            :preview-src-list="[item.before_img]"
            :preview-teleported="true"
          />
         
          <div class="img-infor">
            <span id="myspan1">网络推理图</span>
          </div>
        </div> -->


        <div>
          <div v-if="item.type!=='孪生分类'">
            <el-image
              ref="tableTab"
              class="img-display"
              :src="item.netmap"
              :fit="fit"
              :lazy="true"
              :preview-src-list="[item.netmap]"
              :preview-teleported="true"
            />
            <div class="img-infor">
              <span id="myspan2">网络推理图</span>
              <span
                @click="
                  downloadimgWithWords(
                    item.id,
                    item.netmap,
                    `${item.type}结果图.png`
                  )
                "
              ><i class="iconfont icon-xiazai" /></span>
            </div>
          </div>
          <div
            v-else
            class="img-index"
          >
            <span class="index-number ">{{ Object.keys(item.data)[0] }}: {{ item.data[Object.keys(item.data)] }}</span>
          </div>
        </div>
      </div>
    </div>
  </el-card>
</template>

<script>
import { downloadimgWithWords } from "@/utils/download.js";

export default {
  name: "Analysis_Show",
  props: {
    imgArr:{
      type:Array,
      default(){
        return []
      }
    }
  },
  data() {
    return {
      fit: "fill",
      childImgArr:[],
    };
  },
  mounted() {
    this.childImgArr = this.imgArr
    // console.log(this.childImgArr)
  },
  updated() {
    this.childImgArr = this.imgArr
    // console.log(this.childImgArr)
  },
  methods: {
    downloadimgWithWords,
  },
};
</script>

<style scoped lang="less">
* {
  font-family: SimHei sans-serif;
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
  height: 30px;
  line-height: 30px;
  font-weight: 500;
  font-family: Microsoft JhengHei UI, sans-serif;
}
.img-display-box{
  display: flex;
  flex-direction: column;
  .img-display-item{
    display: flex;
    flex-direction: row;
    justify-content: space-evenly;
    flex-wrap: wrap;
    .img-index{
      line-height: 21rem;
    }
  .img-display{
    width:21rem;
    height: 21rem;
  }
    .img-divider{
      align-items: center;
    }
  }
}
.el-divider /deep/{
  background-color: white;
}
</style>