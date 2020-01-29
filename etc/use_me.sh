
this_file=$(python3 -c 'import os,sys; print(os.path.realpath(sys.argv[1]))' $BASH_SOURCE)

package_base=$(cd $(dirname ${this_file})/.. ; pwd)

export PATH=$package_base/bin${PATH:+:${PATH}}

echo "You can now use the tools $(ls $package_base/bin)"

