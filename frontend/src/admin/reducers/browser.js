import { combineReducers } from 'redux'

import {RECEIVE_DIRECTORY_CONTENT, CHANGE_FILE_BROWSER_SETTINGS, SELECT_FILES, TOGGLE_FILES_SELECT} from '../actions/browser'
import {UPLOAD_COMPLETED} from '../actions/uploads'

import {ROOT_PATH_KEY} from '../store'
import {fileListDisplayValues} from '../ui/filebrowser/index'

const getStateKeyForPath = (path) => {
    switch (path) {
        case '':
        case '/':
        case undefined:
            return ROOT_PATH_KEY
        default:
            // remove opening/trailing slashes
            while (path.startsWith('/') || path.endsWith('/')) {
                if (path.startsWith('/')) { path = path.slice(1)}
                if (path.endsWith('/')) { path = path.slice(0, -1)}
            }
            return path
    }
}


const directories = (state={}, action) => {

    const ownKey = getStateKeyForPath(action.path)

    switch (action.type) {

        case RECEIVE_DIRECTORY_CONTENT:
            let {
                parentDirs,
                childrenDirs,
                files,
                ...own
            } = action.contents;
            let updatedDirs = {}

            // create lists of paths for parents and children
            // populates updatedDirs as a side effect
            let parents = parentDirs.map((d) => {
                    let key = getStateKeyForPath(d.path)
                    updatedDirs[key] = {...state[key], ...d}
                    return key
            })

            let children = childrenDirs.map((d) => {
                    let key = getStateKeyForPath(d.path)
                    updatedDirs[key] = {...state[key], ...d}
                    return key
            })

            // add the loaded directory to
            updatedDirs[ownKey] = {
                ...own,
                lastLoaded: new Date(),
                parents,
                children
            }

            return {
                ...state,
                ...updatedDirs
            }
        default:
            return state

    }
}

const files = (state={}, action) => {
    const fileDefaults = {
        selected: false
    }
    let key = getStateKeyForPath(action.path)
    switch (action.type) {
        case RECEIVE_DIRECTORY_CONTENT:
            let {
                files
            } = action.contents;

            // patch in defaults
            files = files.map((f) => ({
                ...fileDefaults,
                ...f
            }))

            return {
                ...state,
                [key]: [...files]
            }
        case TOGGLE_FILES_SELECT:
            let updatedFiles = state[key].map((f) => {
                if (action.files.includes(f.name)) {
                    return {
                        ...f,
                        selected: !f.selected
                    }
                }
                return f

            })
            return {
                ...state,
                [key]: updatedFiles
            }
        case UPLOAD_COMPLETED:
            let existing_files = state[key] || []
            return {
                ...state,
                [key]: [
                    ...existing_files,
                    action.response
                ]
            }
        default:
            return state
    }
}

// this is being used to hold filebrowser settings
const settings = (
    state={
        selectedDisplayType: fileListDisplayValues[0],
        availableDisplayTypes: fileListDisplayValues
    },
    action) => {
    switch (action.type) {
        case CHANGE_FILE_BROWSER_SETTINGS:
            return {
                ...state,
                ...action.payload
            }
        default:
            return state
    }
}



const filebrowser = combineReducers({
    directories,
    files,
    settings
})

export default filebrowser
export {getStateKeyForPath}
