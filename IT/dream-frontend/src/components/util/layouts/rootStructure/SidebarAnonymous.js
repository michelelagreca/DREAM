import { Icon } from '@iconify/react';
import loginFill from '@iconify/icons-eva/log-in-fill'
import pieChart2Fill from '@iconify/icons-eva/pie-chart-2-fill';
import peopleFill from '@iconify/icons-eva/people-fill';
import shoppingBagFill from '@iconify/icons-eva/shopping-bag-fill';
import fileTextFill from '@iconify/icons-eva/file-text-fill';
import lockFill from '@iconify/icons-eva/lock-fill';
import personAddFill from '@iconify/icons-eva/person-add-fill';
import alertTriangleFill from '@iconify/icons-eva/alert-triangle-fill';
import React from "react";
import NavSection from "../../NavSection";

// ----------------------------------------------------------------------
// find icons here: https://icon-sets.iconify.design/
const getIcon = (name) => <Icon icon={name} width={22} height={22} />;

const sideBarConfig = [
  {
    title: 'forum',
    path: '/forum',
    icon: getIcon(peopleFill)
  },
  {
    title: 'login',
    path: '/login',
    icon: getIcon(loginFill)
  },
  {
    title: 'register',
    path: '/register',
    icon: getIcon(personAddFill)
  }
];

const SidebarAnonymous = ()=>{
  return <NavSection navConfig={sideBarConfig}/>
}

export default SidebarAnonymous;
