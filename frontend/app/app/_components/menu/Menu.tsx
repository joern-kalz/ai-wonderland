export interface MenuProps {
    onStart: () => void;
    isLoading: boolean;
}

export default function Menu({ onStart, isLoading }: MenuProps) {
    return (
        <div>
            <button
                className="p-4 bg-blue-200 hover:bg-blue-300 active:bg-blue-300-300 text-blue-900 active:text-blue-800 border border-gray-400 active:border-gray-500 rounded-md w-50 m-3 cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed"
                onClick={onStart}
                disabled={isLoading}>
                {isLoading ? (
                    <div className="animate-spin h-4 w-4 border border-current border-t-transparent rounded-full mx-auto"></div>
                ) : (
                    'Enter Wonderland'
                )}
            </button>
        </div>
    )
}