#!/bin/bash

#---------------------------------------------------
# Constants
#---------------------------------------------------
NONE='\x1B[0m'
GREEN='\x1B[38;2;64;255;64m'
BLUE='\x1B[38;2;64;64;255m'
RED='\x1B[38;2;255;64;64m'

#---------------------------------------------------
# Functions
#---------------------------------------------------
function exec_cmd {
    msg="$1"
    cmd="$2"
    printf "\n${BLUE}=======================${NONE}\n"
    printf "${BLUE}${msg}${NONE}\n"
    printf "${BLUE}=======================${NONE}\n"
    eval "$cmd"
    if [ $? -eq 0 ] ; then
        printf "${GREEN}[OK]${NONE}\n"
    else
        printf "${RED}[ERROR]${NONE}\n"
        exit 99
    fi
}

#---------------------------------------------------
# Locals
#---------------------------------------------------
VENV_DIR='venv'
IDEA_DIR='.idea'

#---------------------------------------------------
# Arguments
#---------------------------------------------------
FORCE=0
REINIT=0
for i in $(seq $#) ; do
    if [[ "${!i}" == '--force' ]] ; then
        FORCE=1
    fi
    if [[ "${!i}" == '--reinit-code' ]] ; then
        REINIT=1
    fi
done

#---------------------------------------------------
# REINIT USER CODE
#---------------------------------------------------
if [ ${REINIT} -eq 1 ] ; then
    printf "\n${BLUE}=======================${NONE}\n"
    printf "${BLUE}Reinit User Code${NONE}\n"
    printf "${BLUE}=======================${NONE}\n"
    cp -f './core/DO_NOT_TOUCH/.ref_main_code' './Launcher.py'
    cp -f './core/DO_NOT_TOUCH/.ref_user_code' './process.py'
fi

#---------------------------------------------------
# search for newest python
#---------------------------------------------------
NEWEST_EXEC=''
NEWEST_VERS=''
executables=$(compgen -c 'python')
for exec in $executables ; do
    pth=$(which ${exec})
    typ=$(file ${pth} | grep -i 'ELF' )
    if ! [ -z "${typ}" ] ; then
        version=$(eval "${exec} --version 2>&1")
        compare=$(printf "${version}\n${NEWEST_VERS}\n" | sort -t. -k1,1n -k2,2n -k3,3n -k4,4n | tail -n-1)
        if [[ "${compare}" != "${NEWEST_VERS}" ]] ; then
            NEWEST_VERS=${version}
            NEWEST_EXEC=${exec}
        fi
    fi
done
printf "\n${BLUE}=======================${NONE}\n"
printf "${BLUE}Found ${NEWEST_VERS}${NONE}\n"
printf "${BLUE}=======================${NONE}\n"

#---------------------------------------------------
# check if venv exists
#---------------------------------------------------
echo "Checking venv ..."
if [ -d "${VENV_DIR}" ] && [ $FORCE -eq 0 ]; then
    echo "[ERROR] VENV directory already exists !"
    echo "Use --force to replace current venv !"
    exit 1
else
    if [ $FORCE -eq 1 ] ; then
        echo "Removing venv ..."    
        rm -rf ${VENV_DIR}    
    fi
    echo "Creating venv ..."
    eval "${NEWEST_EXEC} -m venv ${VENV_DIR}"
    if [ $? -ne 0 ] ; then
        exit 1
    fi
fi

#---------------------------------------------------
# enable virtual environment
#---------------------------------------------------
echo "Enabling virtual env ..."
source "${VENV_DIR}/bin/activate"

#---------------------------------------------------
# update pip and setuptools
#---------------------------------------------------
msg='Upgrading pip'
cmd='python3 -m pip install --upgrade pip'
exec_cmd "${msg}" "${cmd}"

msg='"Upgrading setuptools'
cmd='python3 -m pip install --upgrade setuptools'
exec_cmd "${msg}" "${cmd}"

# install libs
msg='Installing requirements (arcade + ...)'
cmd='python3 -m pip install -r ./core/requirements.txt'
exec_cmd "${msg}" "${cmd}"

echo ""

