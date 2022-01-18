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
import questionFill from "@iconify/icons-eva/question-mark-circle-fill";
import paperPlaneFill from "@iconify/icons-eva/paper-plane-fill";
import messageCircle from "@iconify/icons-eva/message-circle-fill";
import priceTagFill from "@iconify/icons-eva/pricetags-fill";
import mailFill from "@iconify/icons-eva/email-fill";
import layerFill from "@iconify/icons-eva/layers-fill";
import calendarFill from "@iconify/icons-eva/calendar-fill";
import trendingUpFill from "@iconify/icons-eva/trending-up-fill";

// ----------------------------------------------------------------------
// find icons here: https://icon-sets.iconify.design/
const getIcon = (name) => <Icon icon={name} width={22} height={22} />;

const sideBarConfig = [
  {
    title: 'forum',
    path: '/agronomist/forum',
    icon: getIcon(peopleFill)
  },
  {
    title: 'help requests',
    path: '/agronomist/incoming-hr',
    icon: getIcon(messageCircle)
  },
  {
    title: 'FAQ',
    path: '/agronomist/faq',
    icon: getIcon(priceTagFill)
  },
  {
    title: 'visit plan',
    path: '/agronomist/visit-plan',
    icon: getIcon(calendarFill)
  },
  {
    title: 'visit messages',
    path: '/agronomist/visit-messages',
    icon: getIcon(mailFill)
  },
  {
    title: 'farmers KPIs',
    path: '/agronomist/farmers-kpis',
    icon: getIcon(trendingUpFill)
  },
];

const SideBarAgronomist = ()=>{
  return <NavSection navConfig={sideBarConfig}/>
}

export default SideBarAgronomist;
