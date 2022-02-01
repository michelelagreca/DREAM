import { Icon } from '@iconify/react';
import React, {useEffect, useRef, useState} from 'react';
import editFill from '@iconify/icons-eva/bulb-fill';
import { Link as RouterLink } from 'react-router-dom';
import moreVerticalFill from '@iconify/icons-eva/more-vertical-fill';
// material
import {Menu, MenuItem, IconButton, ListItemIcon, ListItemText, Box} from '@mui/material';
import star from '@iconify/icons-eva/star-fill'
import remove from '@iconify/icons-eva/close-square-fill'
import like from "@iconify/icons-eva/arrow-circle-up-fill";
import dislike from "@iconify/icons-eva/arrow-circle-down-fill";
import none from "@iconify/icons-eva/arrow-back-fill";
import Stack from "@mui/material/Stack";

// ----------------------------------------------------------------------

export default function AnswerLikeMenu({isUserLike, isUserDislike, handleLike, handleDislike, handleRemove}) {
    const ref = useRef(null);
    const [isOpen, setIsOpen] = useState(false);

    const handleLikeWrp = ()=>{
        setIsOpen(false)
        handleLike()
    }
    const handleDislikeWrp = ()=>{
        setIsOpen(false)
        handleDislike()
    }
    const handleRemoveWrp = ()=>{
        setIsOpen(false)
        handleRemove()
    }

    return (
        <>
            <IconButton ref={ref} onClick={() => setIsOpen(true)}>
                <Icon icon={moreVerticalFill} width={20} height={20} />
            </IconButton>

            <Menu
                open={isOpen}
                anchorEl={ref.current}
                onClose={() => setIsOpen(false)}
                PaperProps={{
                    sx: { width: 200, maxWidth: '100%' }
                }}
                anchorOrigin={{ vertical: 'top', horizontal: 'right' }}
                transformOrigin={{ vertical: 'top', horizontal: 'right' }}
            >

                <MenuItem component={RouterLink} to="#" sx={{ color: 'text.secondary' }}>
                    {
                        isUserLike ?
                            <ListItemIcon>
                                <Box sx={{color: 'red', display: 'flex', alignItems: 'center'}}>
                                    <Icon icon={remove} width={20} height={25}/>
                                </Box>
                            </ListItemIcon>
                            : isUserDislike ?
                            <ListItemIcon>
                                <Box sx={{color: 'red', display: 'flex', alignItems: 'center'}}>
                                    <Icon icon={remove} width={20} height={25}/>
                                </Box>
                            </ListItemIcon>
                            : null
                    }
                    {

                        isUserLike || isUserDislike?
                            <ListItemText primary="Remove vote" primaryTypographyProps={{variant: 'body2'}} onClick={handleRemoveWrp}/>
                            : null
                    }
                </MenuItem>
                <MenuItem component={RouterLink} to="#" sx={{ color: 'text.secondary' }}>
                    {
                        !isUserLike && !isUserDislike ?
                            <ListItemIcon>
                                <Box sx={{color: 'gold', display: 'flex',alignItems: 'center'}}>
                                    <Icon icon={like} width={20} height={25} />
                                </Box>
                            </ListItemIcon> : null
                    }
                    {
                        !isUserLike && !isUserDislike ?
                            <ListItemText primary="Vote up" primaryTypographyProps={{variant: 'body2'}} onClick={handleLikeWrp}/> : null
                    }
                </MenuItem>
                <MenuItem component={RouterLink} to="#" sx={{ color: 'text.secondary' }}>
                    {
                        !isUserLike && !isUserDislike ?
                            <ListItemIcon>
                                <Box sx={{color: 'gold', display: 'flex',alignItems: 'center'}}>
                                    <Icon icon={dislike} width={20} height={25} />
                                </Box>
                            </ListItemIcon> : null
                    }
                    {
                        !isUserLike && !isUserDislike ?
                            <ListItemText primary="Vote down" primaryTypographyProps={{variant: 'body2'}} onClick={handleDislikeWrp}/>: null
                    }

                </MenuItem>
            </Menu>
        </>
    );
}
