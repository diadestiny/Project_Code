<template>
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
      prop="date"
      label="目标类别"
      width="180">
    </el-table-column>
    <el-table-column
      prop="name"
      label="目标位置"
      width="180">
    </el-table-column>
    <el-table-column
      prop="address"
      label="置信度">
    </el-table-column>
  </el-table>
</template>

<script>
  export default {
    data() {
      return {
        tableData: [{
          id:'1',
          date: '2016-05-03',
          name: '王小虎',
          address: '上海市普陀区金沙江路 1518 弄'
        }, {
          id:'1',
          date: '2016-05-02',
          name: '王小虎',
          address: '上海市普陀区金沙江路 1518 弄'
        }, {
          id:'1',
          date: '2016-05-04',
          name: '王小虎',
          address: '上海市普陀区金沙江路 1518 弄'
        }]
      }
    }
  }
</script>