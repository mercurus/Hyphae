import { createRouter, createWebHistory, RouteRecordRaw } from "vue-router";
import ViewHome from "../views/ViewHome.vue";

import ViewSearchTopic from "../views/ViewSearchTopic.vue";
import ViewSeeTopic from "../views/ViewSeeTopic.vue";
import ViewEditTopic from "../views/ViewEditTopic.vue";

import ViewSearchMorph from "../views/ViewSearchMorph.vue";
import ViewEditMorph from "../views/ViewEditMorph.vue";

const routes: RouteRecordRaw[] = [
    { 
        path:"/", 
        name:"home", 
        component:ViewHome 
    },

    //TOPICS
    { 
        path:"/topics", 
        name:"searchTopic", 
        component:ViewSearchTopic 
    },
    { 
        path:"/topics/:id", 
        name:"seeTopic", 
        component:ViewSeeTopic, 
        props: route => ({id: route.params.id})
    },
    { 
        path:"/topics/:id/edit", 
        name:"editTopic",
        component:ViewEditTopic,
        props: route => ({id: route.params.id})
    },


    //MORPHS
    { 
        path:"/morphs", 
        name:"searchMorph", 
        component:ViewSearchMorph 
    },
    { 
        path:"/morphs/:id/edit", 
        name:"editMorph", 
        component:ViewEditMorph,
        props: route => ({id: route.params.id})
    },


    // {
    //     path: "/operations",
    //     name: "operationSearch",
    //     component: () => import("@/views/OperationSearch.vue"),
    //     meta: { title:"Search Operations" }
    // },
    // {
    //     path: "/operations/:id",
    //     // name: "operationDetail",
    //     component: () => import("@/views/OperationDetail.vue"),
    //     props: route => ({ id:route.params.id }),
    //     children: [
    //         {
    //             path: "view",
    //             name: "operationDetail.overview",
    //             component: () => import("@/views/OperationDetailOverview.vue"),
    //             props: route => ({ id:route.params.id }),
    //         },
    //         {
    //             path: "cycle/:year",
    //             name: "operationDetail.cycle",
    //             component: () => import("@/views/OperationDetailCycle.vue"),
    //             props: route => ({ id:route.params.id, year:route.params.year }),
    //         },
    //     ],
    // },
    

    // { path:"/topics/:id", name:"articleTopic", component: ()=>import("@/views/ViewArticleTopic.vue") },
    // props: route => ({id: parseInt(route.params.id.toString())})
];

const router = createRouter({
    history: createWebHistory(""), //process.env.BASE_URL
    routes,
  // linkActiveClass: "",
});

// router.beforeEach((to, from, next) => {
//     const title = to.meta?.title;
//     if (title) {
//         (window as any).document.title = title;
//     }
//     next();
// });

export default router;
