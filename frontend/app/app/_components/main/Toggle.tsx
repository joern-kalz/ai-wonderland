export interface Choice {
    children: React.ReactNode;
    onClick: () => void;
    active: boolean;
}

export interface ToggleProps {
    choices: Choice[];
}

export default function Toggle({ choices }: ToggleProps) {
    const buttons = choices.map(({ children, onClick, active }, index) => {
        const rounded = getRoundedClass(index, choices.length);
        const stateStyle = getStateStyle(active);

        return (
            <button
                key={index}
                onClick={onClick}
                className={"flex items-center justify-center w-32 h-12 " +
                    "bg-white text-gray-950 border-1 border-gray-800 border-solid " +
                    `${stateStyle} ${rounded}`}
            >
                {children}
            </button>
        );
    });

    return (<div className="flex">{buttons}</div>)
}

function getStateStyle(active: boolean) {
    if (active) {
        return 'opacity-90 font-bold';
    } else {
        return 'opacity-60 border-opacity-40 hover:opacity-70 hover:border-opacity-60 cursor-pointer';
    }
}

function getRoundedClass(index: number, count: number) {
    if (index === 0) {
        return 'rounded-l-2xl ';
    } else if (index === count - 1) {
        return 'rounded-r-2xl ';
    } else {
        return '';
    }
}