export PYTHONPATH=/nml/nextwheel:/nml/associative_tools

cd /nml/nextwheel/tests

total_tests=0
total_fails=0

for i in *_tests.py; do

    python $i 2> /dev/null;

    if [ $? -eq 0 ]; then
        echo ":) $i"
    else
        echo "F $i"
        let total_fails++
    fi
    let total_tests++
done

echo "$total_tests Tests Run"

if test $total_fails -eq 0; then
    echo "*** ALL PASS ***"
else
    echo "$total_fails Failures"
fi

