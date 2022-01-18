import { Icon } from '@iconify/react';
import pieChart2Fill from '@iconify/icons-eva/pie-chart-2-fill';
import peopleFill from '@iconify/icons-eva/people-fill';
import paperPlaneFill from '@iconify/icons-eva/paper-plane-fill'
import messageCircle from '@iconify/icons-eva/message-circle-fill'
import bulbFill from '@iconify/icons-eva/bulb-fill'
import fileAddFill from '@iconify/icons-eva/file-add-fill'
import priceTagFill from '@iconify/icons-eva/pricetags-fill'
import layerFill from '@iconify/icons-eva/layers-fill'
import loginFill from '@iconify/icons-eva/log-in-fill'
import questionFill from '@iconify/icons-eva/question-mark-circle-fill'
import shoppingBagFill from '@iconify/icons-eva/shopping-bag-fill';
import fileTextFill from '@iconify/icons-eva/file-text-fill';
import lockFill from '@iconify/icons-eva/lock-fill';
import personAddFill from '@iconify/icons-eva/person-add-fill';
import alertTriangleFill from '@iconify/icons-eva/alert-triangle-fill';
import React from "react";
import NavSection from "../../NavSection";
import mailFill from "@iconify/icons-eva/email-fill";

// ----------------------------------------------------------------------
// find icons here: https://icon-sets.iconify.design/
const getIcon = (name) => <Icon icon={name} width={22} height={22} />;

const sideBarConfig = [
  {
    title: 'forum',
    path: '/farmer/forum',
    icon: getIcon(peopleFill)
  },
  {
    title: 'send help request',
    path: '/farmer/send-hr',
    icon: getIcon(paperPlaneFill)
  },
  {
    title: 'help requests',
    path: '/farmer/incoming-hr',
    icon: getIcon(messageCircle)
  },
  {
    title: 'FAQ',
    path: '/farmer/faq',
    icon: getIcon(priceTagFill)
  },
  {
    title: 'Harvest Report',
    path: '/farmer/harvest-rep',
    icon: getIcon(fileAddFill)
  },
  {
    title: 'Harvest history',
    path: '/farmer/harvest-his',
    icon: getIcon(layerFill)
  },
  {
    title: 'incoming Tip Requests',
    path: '/farmer/incoming-tr',
    icon: getIcon(bulbFill)
  },
  {
    title: 'visit messages',
    path: '/farmer/visit-messages',
    icon: getIcon(mailFill)
  },
];

const SidebarFarmer = ()=>{
  return <NavSection navConfig={sideBarConfig}/>
}

export default SidebarFarmer;
