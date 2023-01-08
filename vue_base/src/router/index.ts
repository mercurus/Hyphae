import { createRouter, createWebHistory, RouteRecordRaw } from "vue-router";
import ViewHome from "../views/ViewHome.vue";
import ViewTopicSearch from "../views/ViewTopicSearch.vue";
import ViewMorphSearch from "../views/ViewMorphSearch.vue";

const routes: Array<RouteRecordRaw> = [
    { path:"/", name:"home", component:ViewHome },
    { path:"/topics", name:"topicSearch", component:ViewTopicSearch },
    { path:"/morphs", name:"morphSearch", component:ViewMorphSearch },
];

const router = createRouter({
  history: createWebHistory(""), //process.env.BASE_URL
  routes,
});
  // linkActiveClass: "",

export default router;
