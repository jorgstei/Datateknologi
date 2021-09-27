#!/bin/bash

# Copyright 2013 Benedikt Morbach <moben@exherbo.org>
# Distributed under the terms of the GNU General Public License v2

# runs multiple MPI processes as a grid in a new tmux window and multiplexes keyboard input to all of them

additional_vars=( LD_LIBRARY_PATH LD_PRELOAD )
export "${additional_vars[@]}"

usage() {
    echo 'tmpi: Run multiple MPI processes as a grid in a new tmux window and multiplex keyboard input to all of them.'
    echo ''
    echo 'Usage:'
    echo '   tmpi [number] [command]'
    echo ''
    echo 'You need to pass at least two arguments.'
    echo 'The first argument is the number of processes to use, every argument after that is the commandline to run.'
    echo 'If you call this script from outside tmux and your command contains important whitespace then you need to appy two levels of quoting to preserve it.'
    echo ''
    echo 'LD_LIBRARY_PATH and LD_PRELOAD are passed through, so you can run it like this:'
    echo 'LD_LIBRARY_PATH="${PWD}/.libs:${LD_LIBRARY_PATH}" tmpi 16 gdb -q bin/.libs/example'
    echo ''
    echo 'The new window is set to remain on exit and has to be closed manually. ("C-b + &" by default)'
    echo 'You can use the environment variable TMPI_TMUX_OPTIONS to pass options to the `tmux` invocation, '
    echo '  such as '-f ~/.tmux.conf.tmpi' to use a special tmux configuration for tmpi.'
    echo 'Little usage hint: By default the panes in the window are synchronized. If you wish to work only with one thread maximize this pane ("C-b + z" by default) and work away on one thread. Return to all thread using the same shortcut.'
}

check_tools() {
    tools=( tmux mpirun )

    for tool in "${tools[@]}"; do
        if ! which ${tool}; then
            echo "You need to install ${tool} to run this script."
        fi
    done
}

if [[ ${#} -lt 2 ]]; then
    usage

    exit 1
fi

mpich=$(mpirun --version |grep -i HYDRA)
openmpi=$(mpirun --version |grep -i "Open MPI")

if [ -z "${mpich}" ] && [ -z "${openmpi}" ]; then
    echo "Unknown MPI implementation. Only MPICH (and its derivatives) and OpenMPI are supported!"
    exit 1
fi

if [[ -z ${TMUX} ]]; then
    # it seems we aren't in a tmux session.
    # start a new one so that our window doesn't end up in some other session and we have to search it.
    # actually start a new server with '-L' to ensure that our environment carries over.
    socket=$(mktemp -u tmpi.XXXX)
    exec tmux ${TMPI_TMUX_OPTIONS} -L ${socket} new-session "${0} ${*}"
fi

if [[ ${1} == runmpi ]] ; then
    # we are being started as one of many processes by mpirun.
    shift

    if [ -n "${mpich}" ]; then
        mpi_rank=${PMI_ID}
        mpi_env="-e MPI -e HYD -e PMI"
    else
        mpi_rank=${OMPI_COMM_WORLD_RANK}
        mpi_env="-e MPI -e OPAL -e PMIX"
    fi

    # start the processes in the order of their rank.
    # this avoids races, as we have to push the variables in tmux' environment.
    # it has the nice side-effect that the panes are also ordered by rank.
    while [[ $(cat /tmp/tmpi.lock) -ne ${mpi_rank} ]] ; do
        sleep 0.02
    done

    # get all the variables that mpirun starts us with so that we can pass them through.
    mpi_vars=( $( env | grep ${mpi_env} | cut -d '=' -f1 ) )
    mpi_vars+=( "${additional_vars[@]}" )

    # add the variables to tmux' session environment.
    # we can't just export them because the process will be started as a child of tmux, not us.
    for var in "${mpi_vars[@]}"; do
        tmux set-environment -t ${session} "${var}" "${!var}"
    done

    x=( $(tmux split-window -P -F '#{pane_pid} #{pane_id}' -t ${window} "${*}") )
    pid=${x[0]}
    pane=${x[1]}

    for var in "${mpi_vars[@]}"; do
        tmux set-environment -t ${session} -u "${var}"
    done

    # kill the dummy pane that opened the new window
    [[ ${mpi_rank} -eq 0 ]] && tmux kill-pane -t ${dummy} &> /dev/null

    # set the window to tiled mode.
    # have to do this after every new pane is spawned because otherwise the splits get
    # smaller and smaller until tmux refuses to open new panes, despite plenty of space being left.
    tmux select-layout -t ${pane} tiled &> /dev/null

    # let the next process start
    echo $((${mpi_rank}+1)) > /tmp/tmpi.lock

    # don't exit here as mpirun needs to be kept alive and it would also exit.
    while [[ -d /proc/${pid} ]]; do
        sleep 1
    done
else
    # we are the parent and set everything up before we start ourselves a bunch of times via mpirun.
    processes=${1}
    self=${0}
    shift

    # create an empty new dummy window which we sill later split up for the mpi processes.
    x=( $(tmux new-window ${session} -P -F '#{pane_id} #{window_id} #{session_id}') )
    export dummy=${x[0]}
    export window=${x[1]}
    export session=${x[2]}

    # syncronize input to all panes.
    tmux set-window-option -t ${window} synchronize-panes on &> /dev/null
    #tmux set-window-option -t ${window} remain-on-exit on &> /dev/null

    # always start with rank 0.
    echo 0 > /tmp/tmpi.lock

    pmi_arg=""
    if [ -n "${mpich}" ]; then
        pmi_arg="-pmi-port"
    fi

    # re-execute ourself to spawn of the processes.
    echo mpirun -np ${processes} ${pmi_arg} ${self} runmpi "${@}"
    mpirun -np ${processes} ${pmi_arg} ${self} runmpi "${@}"
fi

