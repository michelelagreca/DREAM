import { Icon } from '@iconify/react';
import pieChart2Fill from '@iconify/icons-eva/pie-chart-2-fill';
import peopleFill from '@iconify/icons-eva/people-fill';
import shoppingBagFill from '@iconify/icons-eva/shopping-bag-fill';
import fileTextFill from '@iconify/icons-eva/file-text-fill';
import lockFill from '@iconify/icons-eva/lock-fill';
import personAddFill from '@iconify/icons-eva/person-add-fill';
import alertTriangleFill from '@iconify/icons-eva/alert-triangle-fill';
import React from "react";
import NavSection from "../../NavSection";
import trendingUpFill from '@iconify/icons-eva/trending-up-fill'
import questionFill from "@iconify/icons-eva/question-mark-circle-fill";
import paperPlaneFill from "@iconify/icons-eva/paper-plane-fill";
import messageCircle from "@iconify/icons-eva/message-circle-fill";
import priceTagFill from "@iconify/icons-eva/pricetags-fill";
import fileAddFill from "@iconify/icons-eva/file-add-fill";
import layerFill from "@iconify/icons-eva/layers-fill";
import bulbFill from "@iconify/icons-eva/bulb-fill";

// ----------------------------------------------------------------------
// find icons here: https://icon-sets.iconify.design/
const getIcon = (name) => <Icon icon={name} width={22} height={22} />;

const sideBarConfig = [
  {
    title: 'forum',
    path: '/policyMaker/forum',
    icon: getIcon(peopleFill)
  },
  {
    title: 'farmers KPIs',
    path: '/policyMaker/farmer-kpis',
    icon: getIcon(trendingUpFill)
  },
  {
    title: 'Tip Requests',
    path: '/policyMaker/send-tr',
    icon: getIcon(bulbFill)
  }
];


const SidebarPolicyMaker = () =>{
  return <NavSection navConfig={sideBarConfig}/>
}
export default SidebarPolicyMaker;
