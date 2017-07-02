/**
 * Created by sean on 09/02/17.
 */

export const REQUEST_DIRECTORY = 'REQUEST_DIRECTORY'
export const RECEIVE_DIRECTORY_CONTENT = 'RECEIVE_DIRECTORY_CONTENT'
export const CHANGE_FILE_BROWSER_SETTINGS = 'CHANGE_FILE_BROWSER_SETTINGS'

export const TOGGLE_FILES_SELECT = 'TOGGLE_FILES_SELECT'
export const TOGGLE_FILES_SELECT_ALL = 'TOGGLE_FILES_SELECT_ALL'

import {requestDirectory} from '../api/browser'

export const toggleSelect = (path, files, modifiers) => {
    return {
        type: TOGGLE_FILES_SELECT,
        path,
        files,
        modifiers
    }
}

export const toggleSelectAll = (path, select) => {
    return {
        type: TOGGLE_FILES_SELECT_ALL,
        path,
        select
    }
}

export const requestDirectoryAction = (path, url) => {
    return (dispatch) => {
        dispatch({
            type: REQUEST_DIRECTORY,
            path,
            url
        });
        requestDirectory(url).then((data) => {
            dispatch({
                type: RECEIVE_DIRECTORY_CONTENT,
                payload: data,
                path,
                url
            })
        })
    }
}


export const switchFilebrowserDisplayType = (displayType) => {
    return {
        type: CHANGE_FILE_BROWSER_SETTINGS,
        payload: {
            selectedDisplayType: displayType
        }
    }
}


