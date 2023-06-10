<script>
const BASEURL = "http://"+process.env.VUE_APP_BACKEND_IP+":"+process.env.VUE_APP_BACKEND_PORT+"/"
const BACKEND_URL = BASEURL + "/code/backend/static/"
export default {
  BASEURL, BACKEND_URL
};
</script>

