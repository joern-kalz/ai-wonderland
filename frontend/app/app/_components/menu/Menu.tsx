export interface MenuProps {
    onStart: () => void;
}

export default function Menu({ onStart }: MenuProps) {
    return (
        <div>
            <button
                className="p-4 bg-blue-200 hover:bg-blue-300 active:bg-blue-300-300 text-blue-900 active:text-blue-800 border border-gray-400 active:border-gray-500 rounded-md w-50 m-3 cursor-pointer"
                onClick={onStart}>
                Enter Wonderland
            </button>
        </div>
    )
}