import { Icon } from '@iconify/react';
import React, { useRef, useState } from 'react';
import editFill from '@iconify/icons-eva/bulb-fill';
import { Link as RouterLink } from 'react-router-dom';
import moreVerticalFill from '@iconify/icons-eva/more-vertical-fill';
// material
import {Menu, MenuItem, IconButton, ListItemIcon, ListItemText, Box} from '@mui/material';
import star from '@iconify/icons-eva/star-fill'
import remove from '@iconify/icons-eva/close-square-fill'

// ----------------------------------------------------------------------

export default function TipMoreMenu({isStar, setIsStar}) {
    const ref = useRef(null);
    const [isOpen, setIsOpen] = useState(false);

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
                    <ListItemIcon>
                        {
                            isStar ?
                                <Box sx={{color: 'red', display: 'flex',alignItems: 'center'}}>
                                    <Icon icon={remove} width={20} height={25} />
                                </Box>
                                :
                                <Box sx={{color: 'gold', display: 'flex',alignItems: 'center'}}>
                                    <Icon icon={star} width={20} height={25} />
                                </Box>

                        }
                    </ListItemIcon>
                    {
                        isStar ?
                            <ListItemText primary="Remove Star" primaryTypographyProps={{variant: 'body2'}} onClick={()=>setIsStar(false)}/>
                            :
                            <ListItemText primary="Promote to Star" primaryTypographyProps={{variant: 'body2'}} onClick={()=>setIsStar(true)}/>
                    }
                </MenuItem>
            </Menu>
        </>
    );
}
